from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        if isinstance(exc, ValidationError):
            if isinstance(response.data, list):
                response.data = {"error": response.data[0]}
            elif isinstance(response.data, dict):
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