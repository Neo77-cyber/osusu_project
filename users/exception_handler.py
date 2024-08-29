from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Customize the response for different error statuses
        if response.status_code == 400:
            response.data = {
                'error': 'Bad Request',
                'details': response.data
            }
        elif response.status_code == 404:
            response.data = {
                'error': 'Not Found',
                'details': 'The requested resource was not found.'
            }
        elif response.status_code == 500:
            response.data = {
                'error': 'Internal Server Error',
                'details': 'An unexpected error occurred. Please try again later.'
            }

    return response
