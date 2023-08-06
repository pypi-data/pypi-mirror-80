from src.class_serializer.serializable import serialize, Serializable


class Bar(Serializable):
    def __init__(
            self,
            _id: int
    ):
        self.__id = _id

    @serialize()
    def id(self) -> int:
        return self.__id
