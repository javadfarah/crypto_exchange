from django.http import JsonResponse

from .general_exception import GeneralException, status


class EntityException(GeneralException):
    def __init__(self, message: str, error_code: int = 1):
        super(EntityException, self).__init__(message=message, error_code=error_code)

    def response(self) -> JsonResponse:
        exp_data = {
            "error": "Entity Exception",
            "message": self.message,
            "type": self.code_reference[self.error_code]
            if self.error_code in self.code_reference
            else self.error_code,
        }
        if self.error_code == status.DOES_NOT_EXIST_ERROR:
            return JsonResponse(data=exp_data, status=404)
        return JsonResponse(data=exp_data, status=400)
