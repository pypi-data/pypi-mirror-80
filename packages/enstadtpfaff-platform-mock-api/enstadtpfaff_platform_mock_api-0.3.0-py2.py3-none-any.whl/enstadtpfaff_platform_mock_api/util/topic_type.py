from enum import Enum

from .constants import CONST


class TopicType(Enum):
    SHARED = CONST.SHARED_TOPIC
    SERVICE_SPECIFIC = CONST.SERVICE_TOPIC
