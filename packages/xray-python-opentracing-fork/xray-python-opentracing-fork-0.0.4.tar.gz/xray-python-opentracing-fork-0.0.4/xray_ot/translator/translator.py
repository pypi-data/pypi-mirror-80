from typing import Callable, Dict, Union, Optional

from basictracer.span import BasicSpan, LogData
from opentracing.logs import ERROR_OBJECT

from ..rand import generate_64bit_id_as_hex
from ..settings import RecordingSettings
from . import components as component_processors
from .ot_types import T_TAGS, T_XRAY_TAGS

T_COMPONENT_PROCESSOR = Callable[[RecordingSettings, T_TAGS], T_XRAY_TAGS]


def preprocess_component_tags(component: str, tags: T_TAGS) -> T_TAGS:
    """
    Strip the prefixes from the tags.

    Example 1:
        >>> tags: T_TAGS = {"http.url": "https://example.com/", "http.method": "POST"}
        >>> preprocess_component_tags(tags)
        >>> -> {"url": "https://example.com/", "method": "POST"}

    Example 2: removing other component fields, such as error[.object]
        >>> tags: T_TAGS = {"http.method": "POST", "error": True, "error.object": ...}
        >>> preprocess_component_tags(tags)
        >>> -> {"method": "POST"}

    """
    translation = {}
    tag_prefix_len = len(component)
    tag_prefix_len_with_sep = tag_prefix_len + 1  # {component} + '.'

    for tag_name, value in tags.items():
        # Skip the tag if it doesn't match the component name
        if len(tag_name) <= tag_prefix_len_with_sep:
            continue

        tag_prefix, tag_name = (
            tag_name[:tag_prefix_len],
            tag_name[tag_prefix_len_with_sep:],
        )

        # Skip the tag if it doesn't match the component name
        if tag_prefix != component:
            continue

        translation[tag_name] = value

    return translation


class Translator:
    def __init__(self, settings: RecordingSettings):
        self.settings = settings

    @classmethod
    def translate(cls, *, settings: RecordingSettings, span: BasicSpan) -> T_XRAY_TAGS:
        translator = cls(settings)
        payload = translator.process_component(span.tags)
        payload.update(translator.process_errors(span))
        return payload

    def process_component(self, tags: T_TAGS) -> Dict[str, T_TAGS]:
        component: str = tags.pop("component", "")
        translator = None

        if component:
            tags = preprocess_component_tags(component, tags)
            translator = self.get_component_translator(component)

        if translator is not None:
            translation = translator(self.settings, tags)
        else:
            translation = {
                "annotations": {
                    f"{component}_{tag}": value for tag, value in tags.items()
                }
            }
        return translation

    @staticmethod
    def process_errors(span: BasicSpan) -> Union[Dict, T_XRAY_TAGS]:
        results = {}

        if not span.tags.get("error", False):
            return results

        log: LogData
        error_obj = None

        for log in span.logs:
            error_obj: Optional[Exception] = log.key_values.get(ERROR_OBJECT, None)

        if error_obj is not None:
            # 5XX
            exception = {
                "id": generate_64bit_id_as_hex(),
                "message": str(error_obj),
                "type": error_obj.__class__.__name__,
            }
            results["fault"] = True
            results["exception"] = exception
        else:
            # 4XX
            results["error"] = True

        return results

    @staticmethod
    def get_component_translator(component) -> T_COMPONENT_PROCESSOR:
        translator: T_COMPONENT_PROCESSOR = getattr(
            component_processors, component, None
        )
        return translator
