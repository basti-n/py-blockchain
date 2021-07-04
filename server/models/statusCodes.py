from enum import Enum


class HttpStatusCodes(int, Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    CONFLICT = 409
    SERVER_ERROR = 500
