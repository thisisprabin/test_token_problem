from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {
            "code": response.status_code,
            "message": response.data["detail"],
            "error_type": exc.default_code,
            "data": None,
        }

    return response
