from xray_ot.settings import RecordingSettings
from xray_ot.translator.ot_types import T_TAGS, T_XRAY_TAGS


def http(settings: RecordingSettings, tags: T_TAGS) -> T_XRAY_TAGS:
    request = {}
    response = {}

    for tag_name, tag_value in tags.items():
        obj = response

        if tag_name in settings.http_request_annotations:
            obj = request
            tag_name = settings.http_request_annotations[tag_name]

        elif tag_name in settings.http_response_annotations:
            tag_name = settings.http_response_annotations[tag_name]

        obj[tag_name] = tag_value

    return {
        "http": {
            "request": request,
            "response": response,
        }
    }
