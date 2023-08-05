"""
AWS X-Ray backed implementation of the python OpenTracing API.

https://github.com/opentracing/basictracer-python

See the API definition for comments.
"""

import atexit
import sys
import threading
import time
import traceback
import warnings
from typing import List

from basictracer.recorder import SpanRecorder
from basictracer.span import BasicSpan

from . import connection as conn
from . import constants
from .settings import RecordingSettings
from .translator import Translator


class Recorder(SpanRecorder):
    """Recorder translates, buffers, and reports basictracer.BasicSpans.

    These reports are sent to an X-Ray daemon at the provided address.

    For parameter semantics, see Tracer() documentation; Recorder() respects
    component_name, collector_host, collector_port, tags, max_span_records,
    periodic_flush_seconds, verbosity
    """

    def __init__(
        self,
        component_name=None,
        collector_host="127.0.0.1",
        collector_port=2000,
        settings: RecordingSettings = None,
        max_span_records=constants.DEFAULT_MAX_SPAN_RECORDS,
        periodic_flush_seconds=constants.FLUSH_PERIOD_SECS,
        verbosity=0,
    ):
        self.verbosity = verbosity
        self._collector_address = (collector_host, collector_port)

        self.component_name = component_name if component_name is None else sys.argv[0]
        self.settings = settings if settings is not None else RecordingSettings()

        self._mutex = threading.Lock()
        self._span_records = []
        self._max_span_records = max_span_records

        self._disabled_runtime = False
        atexit.register(self.shutdown)

        self._periodic_flush_seconds = periodic_flush_seconds
        # _flush_connection and _flush_thread are created lazily since some
        # Python environments (e.g., Tornado) fork() initially and mess up the
        # reporting machinery up otherwise.
        self._flush_connection = None
        self._flush_thread = None
        if self._periodic_flush_seconds <= 0:
            warnings.warn(
                f"Runtime(periodic_flush_seconds={self._periodic_flush_seconds}) "
                f"means we will never flush to xray daemon unless explicitly requested."
            )

    def _maybe_init_flush_thread(self) -> None:
        """Start a periodic flush mechanism for this recorder if:

        1. periodic_flush_seconds > 0, and 
        2. self._flush_thread is None, indicating that we have not yet
           initialized the background flush thread.

        We do these things lazily because things like `tornado` break if the
        background flush thread starts before `fork()` calls happen.
        """
        if (self._periodic_flush_seconds > 0) and (self._flush_thread is None):
            self._flush_connection = conn.XRayConnection(self._collector_address)
            self._flush_thread = threading.Thread(
                target=self._flush_periodically, name=constants.FLUSH_THREAD_NAME
            )
            self._flush_thread.daemon = True
            self._flush_thread.start()

    def _fine(self, fmt, args) -> None:
        if self.verbosity >= 1:
            print("[X-Ray Tracer]:", (fmt % args))

    def _finest(self, fmt, args) -> None:
        if self.verbosity >= 2:
            print("[X-Ray Tracer]:", (fmt % args))

    def record_span(self, span) -> None:
        """Per BasicSpan.record_span, safely add a span to the buffer.

        Will drop a previously-added span if the limit has been reached.
        """
        if self._disabled_runtime:
            return

        # Lazy-init the flush loop (if need be).
        self._maybe_init_flush_thread()

        # Checking the len() here *could* result in a span getting dropped that
        # might have fit if a report started before the append(). This would only
        # happen if the client lib was being saturated anyway (and likely
        # dropping spans). But on the plus side, having the check here avoids
        # doing a span conversion when the span will just be dropped while also
        # keeping the lock scope minimized.
        with self._mutex:
            if len(self._span_records) >= self._max_span_records:
                return

        segment = {
            "trace_id": span.context.trace_id,
            "id": span.context.span_id,
            "start_time": span.start_time,
            "end_time": span.start_time + span.duration,
            "name": span.operation_name,
        }

        if span.parent_id is not None:
            segment["parent_id"] = span.parent_id
            segment["type"] = "subsegment"
        if span.tags:
            segment.update(Translator.translate(settings=self.settings, span=span))

        if len(span.logs) > 0:
            logs = [
                {"timestamp": log.timestamp, "fields": log.key_values}
                for log in span.logs
            ]
            segment["metadata"] = {"logs": logs}

        with self._mutex:
            if len(self._span_records) < self._max_span_records:
                self._span_records.append(segment)

    def flush(self, connection=None) -> bool:
        """Immediately send unreported data to the daemon.

        Calling flush() will ensure that any current unreported data will be
        immediately sent to the host server.

        If connection is not specified, the report will sent to the server
        passed in to __init__.  Note that custom connections are currently used
        for unit testing against a mocked connection.

        Returns whether the data was successfully flushed.
        """
        if self._disabled_runtime:
            return False

        if connection is not None:
            return self._flush_worker(connection)
        else:
            self._maybe_init_flush_thread()
            return self._flush_worker(self._flush_connection)

    def shutdown(self, flush=True) -> bool:
        """Shutdown the Runtime's connection by (optionally) flushing the
        remaining logs and spans and then disabling the Runtime.

        Note: spans and logs will no longer be reported after shutdown is called.

        Returns whether the data was successfully flushed.
        """
        # Closing connection twice results in an error. Exit early
        # if runtime has already been disabled.
        if self._disabled_runtime:
            return False

        flushed = flush and self.flush()
        self._disabled_runtime = True
        return flushed

    def _flush_periodically(self) -> None:
        """Periodically send reports to the server.

        Runs in a dedicated daemon thread (self._flush_thread).
        """
        # Send data until we get disabled
        while not self._disabled_runtime:
            self._flush_worker(self._flush_connection)
            time.sleep(self._periodic_flush_seconds)

    def _flush_worker(self, connection) -> bool:
        """Use the given connection to transmit the current logs and spans as a
        report request."""
        if connection is None:
            return False

        report_request = self._construct_report_request()
        try:
            self._finest("Sending report to daemon: %s", (report_request,))
            connection.report(report_request)

            return True

        except Exception as e:
            self._fine(
                "Caught exception during report: %s, stack trace: %s",
                (e, traceback.format_exc()),
            )
            self._restore_spans(report_request)
            return False

    def _construct_report_request(self) -> List[BasicSpan]:
        """Construct a report request."""
        with self._mutex:
            records = self._span_records
            self._span_records = []
        return records

    def _restore_spans(self, span_records) -> None:
        """Called after a flush error to move records back into the buffer
        """
        if self._disabled_runtime:
            return

        with self._mutex:
            if len(self._span_records) >= self._max_span_records:
                return
            combined = span_records + self._span_records
            self._span_records = combined[-self._max_span_records :]
