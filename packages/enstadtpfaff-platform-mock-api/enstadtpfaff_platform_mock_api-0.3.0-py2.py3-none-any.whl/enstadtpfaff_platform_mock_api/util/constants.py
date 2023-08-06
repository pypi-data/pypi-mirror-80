class _Const:
    @property
    def TOPIC_ROOT(self):
        return "platform-mock"

    @property
    def SHARED_TOPIC(self):
        return "shared"

    @property
    def SERVICE_TOPIC(self):
        return "services"

    @property
    def TOPIC_LEVEL_SEPARATOR(self):
        return "/"


CONST = _Const()
