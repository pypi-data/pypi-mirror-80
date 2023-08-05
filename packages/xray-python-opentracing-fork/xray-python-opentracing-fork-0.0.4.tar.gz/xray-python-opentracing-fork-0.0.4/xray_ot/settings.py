from dataclasses import dataclass, field
from typing import Dict


def default_field(obj):
    return field(default_factory=lambda: obj)


@dataclass(frozen=True)
class RecordingSettings:
    db_annotations: Dict[str, str] = default_field(
        {
            "statement": "sanitized_query",
            "type": "database_type",
            # Implicit Associations:
            # db.user -> user
        }
    )

    http_request_annotations: Dict[str, str] = default_field(
        {
            "method": "method",
            "url": "url",
            "client_ip": "client_ip",
            "user_agent": "user_agent",
        }
    )

    http_response_annotations: Dict[str, str] = default_field({"status_code": "status"})
