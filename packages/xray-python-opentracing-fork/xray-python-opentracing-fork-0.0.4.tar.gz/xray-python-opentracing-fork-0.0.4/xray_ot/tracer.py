"""
AWS X-Ray backed implementation of the python OpenTracing API.

http://opentracing.io
https://github.com/opentracing/api-python

See the API definition for comments.
"""
from __future__ import absolute_import

import binascii
import os
import time

from basictracer import BasicTracer
from opentracing import Format

from .binary_propagator import BinaryPropagator
from xray_ot.recorder import Recorder
from .rand import generate_64bit_id_as_hex
from .text_propagator import TextPropagator


def Tracer(**kwargs) -> "_XRayTracer":
    """Instantiates the AWS X-Ray OpenTracing implementation.

    :param str component_name: the human-readable identity of the instrumented
        process. I.e., if one drew a block diagram of the distributed system,
        the component_name would be the name inside the box that includes this
        process.
    :param str collector_host: X-Ray daemon hostname
    :param int collector_port: X-Ray daemon port
    :param dict tags: a string->string dict of tags for the Tracer itself (as
        opposed to the Spans it records)
    :param int max_span_records: Maximum number of spans records to buffer
    :param int periodic_flush_seconds: seconds between periodic background
        flushes, or 0 to disable background flushes entirely.
    :param int verbosity: verbosity for (debug) logging, all via logging.info().
        0 (default): log nothing
        1: log transient problems
        2: log all of the above, along with payloads sent over the wire
    """
    return _XRayTracer(Recorder(**kwargs))


class _XRayTracer(BasicTracer):
    def __init__(self, recorder):
        """Initialize the X-Ray Tracer, deferring to BasicTracer."""
        super(_XRayTracer, self).__init__(recorder)
        self.register_propagator(Format.TEXT_MAP, TextPropagator())
        self.register_propagator(Format.HTTP_HEADERS, TextPropagator())
        self.register_propagator(Format.BINARY, BinaryPropagator())

    def flush(self) -> None:
        """Force a flush of buffered Span data to the X-Ray daemon."""
        self.recorder.flush()

    def start_span(self, *args, **kwargs):
        span = super().start_span(*args, **kwargs)
        if span.parent_id is None:
            span.context.trace_id = "1-%x-%s" % (
                int(time.time()),
                binascii.b2a_hex(os.urandom(12)).decode("ascii"),
            )
        span.context.span_id = generate_64bit_id_as_hex()
        return span

    def __enter__(self) -> "_XRayTracer":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.flush()
