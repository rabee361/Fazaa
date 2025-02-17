from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError,APIException


class ErrorResult(APIException):

    def __init__(self, message='error occurred', code="ERROR",status=400):
        self.default_detail=message
        self.default_code=code
        self.status_code=status
        super().__init__(message, code)

    @classmethod
    def serverError(cls):
        return cls('server error','SERVER_ERROR',500)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print(response)
    
    if response is not None:
        print(isinstance(exc, ValidationError))
        if isinstance(exc, ValidationError):
            print(isinstance(response.data, list))
            if isinstance(response.data, list):
                response.data = {"error": response.data[0]}
            elif isinstance(response.data, dict):
                print(response.data)
                # If there's already an "error" key, keep it
                if "error" in response.data:
                    if isinstance(response.data["error"], list):
                        response.data = {"error": response.data["error"][0]}
                else:
                    # Get the first error from any field
                    for field_errors in response.data.values():
                        if isinstance(field_errors, list) and field_errors:
                            response.data = {"error": field_errors[0]}
                            break
                        elif isinstance(field_errors, str):
                            response.data = {"error": field_errors}
                            break
                    else:
                        response.data = {"error": "حدث خطأ"}
    
    return response 