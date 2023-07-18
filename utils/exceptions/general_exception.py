from abc import abstractmethod
import inspect

from django.http import JsonResponse

from . import status


class GeneralException(Exception):
    def __init__(self, message: str, error_code: int = 0, name=""):

        super().__init__(message)
        self.error_code = error_code
        self.message = message
        self.name = name
        self.code_reference = self.load_code_reference()
        print(self.code_reference)

    @abstractmethod
    def response(self) -> JsonResponse:
        pass

    @staticmethod
    def load_code_reference():
        code_reference = {}
        for name, obj in inspect.getmembers(status):
            if inspect.isclass(obj):
                code_reference.update({obj.error_code: obj.message})

        return code_reference
