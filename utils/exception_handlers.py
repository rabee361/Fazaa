from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        # Convert validation errors to {"error": "message"} format
        if isinstance(exc, ValidationError):
            if isinstance(response.data, list):
                response.data = {"error": response.data[0]}
            elif isinstance(response.data, dict):
                if "error" not in response.data:
                    # Take the first error message if multiple exist
                    first_error = next(iter(response.data.values()))[0] if response.data else "حدث خطأ"
                    response.data = {"error": first_error}
    
    return response 