#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from .httpexception import *


class HTTPAuthError(HTTPForbidden):

    def __init__(self):
        super().__init__('auth-error')


class HTTPInvalidParams(HTTPBadRequest):

    def __init__(self):
        super().__init__('invalid-api-parameters')


class HTTPCustomerNotFound(HTTPNotFound):

    def __init__(self):
        super().__init__('customer-not-found')


class HTTPInvalidReference(HTTPNotFound):

    def __init__(self):
        super().__init__('invalid-ref-id')


class HTTPAmountMisMatch(HTTPBadRequest):

    def __init__(self):
        super().__init__('amount-mismatch')
