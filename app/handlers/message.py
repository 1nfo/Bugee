from enum import Enum, auto


class ResponseType(Enum):
    Success = auto()
    InvalidInput = auto()
    InvalidData = auto()
    IncorrectPassword = auto()
    UsernameNotExists = auto()


class Response:
    def __init__(self, result, enum=None, details=None):
        self.result = result
        self.enum = enum
        self.details = details

    @property
    def view_message(self) -> str:
        return str((self.enum.name, self.details))

    @property
    def success(self):
        return self.result is True
