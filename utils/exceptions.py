from rest_framework.views import exception_handler
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response = {
            'error': response.data.get('detail', 'An error occurred.'),
            'details': response.data if isinstance(response.data, dict) else {},
            'status_code': response.status_code,
        }
        response.data = custom_response

    return response
