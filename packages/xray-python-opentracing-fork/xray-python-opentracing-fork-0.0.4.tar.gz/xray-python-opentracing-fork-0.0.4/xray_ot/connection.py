"""Connection class marshals data over UDP to daemon."""
import json
from socket import AF_INET, SOCK_DGRAM, SocketType, socket

from xray_ot.encoder import default_encoder


class XRayConnection(object):
    """
    Instances of _Connection are used to communicate with the X-Ray daemon via UDP.
    """

    def __init__(self, collector_address: (str, int)):
        self._collector_address: str = collector_address
        self._socket: SocketType = socket(AF_INET, SOCK_DGRAM)

    @staticmethod
    def to_payload(msg) -> bytes:
        return (
            '{"format": "json", "version": 1}\n'
            + json.dumps(msg, default=default_encoder)
        ).encode("utf8")

    def report(self, msg) -> None:
        """Report to the daemon."""
        for m in msg:
            self._socket.sendto(self.to_payload(m), self._collector_address)
