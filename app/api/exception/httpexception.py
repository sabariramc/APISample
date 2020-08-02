#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from app.exception import AppException


class HTTPException(AppException):

    def __init__(self, http_error_code, message, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.code = http_error_code
        self.message = message


class HTTPForbidden(HTTPException):
    def __init__(self, message):
        super().__init__(403, message)


class HTTPBadRequest(HTTPException):

    def __init__(self, message):
        super().__init__(400, message)


class HTTPNotFound(HTTPException):

    def __init__(self, message):
        super().__init__(404, message)
