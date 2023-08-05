from xray_ot.settings import RecordingSettings
from xray_ot.translator.ot_types import T_TAGS, T_XRAY_TAGS


def db(settings: RecordingSettings, tags: T_TAGS) -> T_XRAY_TAGS:
    return {
        "sql": {
            (settings.db_annotations.get(tag_name, tag_name)): tag_value
            for tag_name, tag_value in tags.items()
        }
    }
