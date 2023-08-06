from enum import Enum

from enstadtpfaff_platform_mock_api import Event
from enstadtpfaff_platform_mock_api.util import TopicUtil


class Category(Enum):
    NATURE = 'NATURE'
    HOUSEHOLD = 'HOUSEHOLD'
    MOBILITY = 'MOBILITY'
    ENERGY = 'ENERGY'
    FAMILY = 'FAMILY'
    GROCERIES = 'GROCERIES'
    FREETIME = 'FREETIME'
    HEATING = 'HEATING'
    MISC = 'MISC'


# noinspection PyPep8Naming
class Hint:
    def __init__(
            self,
            headline: str,
            content: str,
            categories: list,
            recipients: list = None,
            issuedBy: str = None,
            issuedAt: str = None,
            basedOn: list = None,
            validityBegin: str = None,
            validityEnd: str = None
    ):
        self.headline = headline
        self.content = content
        self.categories = list(
            map((lambda category: category if isinstance(category, str) else category.value), categories)
        )
        self.recipients = recipients
        self.issuedBy = issuedBy
        self.issuedAt = issuedAt
        self.basedOn = basedOn
        self.validityBegin = validityBegin
        self.validityEnd = validityEnd


class Hints:
    SHARED_TOPIC_ID = "hints"
    HINTS_TOPIC = TopicUtil.shared_topic(
        SHARED_TOPIC_ID
    )

    @staticmethod
    def hint(
            hint: Hint
    ) -> Event:
        payload = Hints._del_none(vars(hint))
        return Event(
            Hints.HINTS_TOPIC,
            payload
        )

    @staticmethod
    def _del_none(d):
        """
        Delete keys with the value ``None`` in a dictionary, recursively.
        """
        if not isinstance(d, dict):
            return d
        return dict((k, Hints._del_none(v)) for k, v in d.items() if v is not None)
