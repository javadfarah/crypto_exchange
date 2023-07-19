from django.http import JsonResponse

from .general_exception import GeneralException, status


class UseCaseException(GeneralException):
    def __init__(self, message: str, error_code: int = 1, name=""):
        super(UseCaseException, self).__init__(message=message, error_code=error_code, name=name)

    def response(self) -> JsonResponse:
        exp_data = {
            "error": "UseCase Exception",
            "message": self.message,
            "name": self.name,
            "type": self.code_reference[self.error_code]
            if self.error_code in self.code_reference
            else self.error_code,
        }
        if self.error_code == status.DOES_NOT_EXIST_ERROR:
            return JsonResponse(data=exp_data, status=404)
        return JsonResponse(data=exp_data, status=400)
