from typing import Dict, Union, Any

T_TAGS = Dict[str, Union[str, int, float]]
T_XRAY_TAGS = Dict[str, Union[T_TAGS, Dict[str, Any]]]
