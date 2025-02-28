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
    
    if response is not None and isinstance(exc, ValidationError):
        # Handle list of errors
        if isinstance(response.data, list):
            response.data = {"error": response.data[0]}
            return response
            
        # Handle dict of errors
        if isinstance(response.data, dict):
            # If there's already an error key
            if "error" in response.data:
                if isinstance(response.data["error"], list):
                    response.data = {"error": response.data["error"][0]}
                return response
                
            # Get first error from any field
            for field, errors in response.data.items():
                if isinstance(errors, list) and errors:
                    response.data = {"error": errors[0]}
                    break
                elif isinstance(errors, str):
                    response.data = {"error": errors}
                    break
            else:
                response.data = {"error": "حدث خطأ"}
                
    return response