import sys
from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.exceptions import APIException, ErrorDetail, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import exception_handler


class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Error"
    default_message_key = "error"
    default_errors: dict[str, str] = {}

    def __init__(
        self,
        detail=None,
        code=None,
        message=None,
        message_key=None,
        errors=None,
    ):
        super().__init__(detail, code)
        self.message = message or self.default_message
        self.message_key = message_key or self.default_message_key
        self.errors = errors or self.default_errors



class APIExceptionFormatter:
    @classmethod
    def extract_error_code(cls, errors: Any) -> dict:
        if isinstance(errors, dict):
            for key, value in errors.items():
                if isinstance(value, (list, tuple)):
                    value = value[0]
                    errors[key] = (
                        value.code if isinstance(value, ErrorDetail) else str(value)
                    )
                elif isinstance(value, dict):
                    errors[key] = cls.extract_error_code(value)
                else:
                    errors[key] = str(value)
        return errors

    def __init__(self, exception: APIException):
        self.exception_class = exception.__class__.__name__
        self.detail = exception.detail
        self.default_code = exception.default_code
        self.message = getattr(exception, "message", None) or exception.default_detail
        self.message_key = getattr(exception, "message_key", None) or self.default_code
        self.errors = getattr(exception, "errors", None) or (
            self.detail if isinstance(self.detail, dict) else {}
        )
        if isinstance(self.detail, dict):
            for key, value in self.detail.items():
                if isinstance(value, (list, tuple)):
                    value = value[0]
                    self.detail[key] = (
                        value.code if isinstance(value, ErrorDetail) else str(value)
                    )
                elif isinstance(value, dict):
                    self.detail[key] = {}
                    self.detail[key] = APIExceptionFormatter.extract_error_code(value)
                else:
                    self.detail[key] = str(value)

        if isinstance(exception, MethodNotAllowed):
            self.message = self.detail
            self.message_key = self.default_code
            self.errors = {}

    def get_response(self):
        return {
            "success": False,
            "message": self.message,
            "message_key": self.message_key,
            "errors": self.errors,
            "exception_class": self.exception_class,
        }


def server_error(request, *args, **kwargs):
    exc_type, exc_value, _ = sys.exc_info()
    data = {
        "success": False,
        "message": str(exc_value),
        "message_key": "internal_server_error",
        "errors": {},
        "exception_class": exc_type.__name__,
    }
    return JsonResponse(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def drf_exception_handler(exception, context):
    response = exception_handler(exception, context)
    if isinstance(exception, (Http404, ObjectDoesNotExist)):
        return Response(status=status.HTTP_404_NOT_FOUND)
    if response is not None:
        formatted_exception = APIExceptionFormatter(exception)
        response.data = formatted_exception.get_response()
    return response
