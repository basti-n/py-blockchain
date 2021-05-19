from typing import Dict
from flask import jsonify


class Response:
    """ Class for creating response objects """

    def __init__(self, body: Dict, message: str, status: int):
        self.status = status
        self.data = body | {'message': message} | {'error': self.is_error()}

    def json(self) -> str:
        return jsonify(self.data)

    def get(self):
        return self.json(), self.status

    def is_error(self) -> bool:
        return False if self.status <= 299 and self.status >= 200 else True
