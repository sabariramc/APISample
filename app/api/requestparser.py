#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 08-Jun-2020
"""

from functools import wraps
from datetime import datetime, date
from decimal import Decimal
import re

from flask import request, current_app

from ..utility import is_non_empty_value
from .exception import HTTPInvalidParams, HTTPAuthError


class APIAuth:
    def __call__(self, func_obj):
        @wraps(func_obj)
        def request_checker(*args, **kwargs):
            if request.headers.get('X-API-KEY') and request.headers.get('X-API-KEY') in current_app.api_key:
                return {
                    'status': 'SUCCESS'
                    , 'data': func_obj(*args, **kwargs)
                }
            else:
                raise HTTPAuthError()

        return request_checker


def requires_api_key(fu):
    return APIAuth()(fu)


class ParamValidator:
    def __init__(self, request_definition=None, is_strict=True):
        self.is_strict = is_strict
        self.request_definition = self.validate_type_definition(request_definition)

    def __call__(self, func_obj):
        @wraps(func_obj)
        def request_checker(*args, **kwargs):
            function_argument = self.parser(request.json, self.request_definition)
            kwargs.update(function_argument)
            return func_obj(*args, **kwargs)

        return request_checker

    def parser(self, params, definition, parent=None):
        if is_non_empty_value(params) is False:
            params = {}
        validated_params = {}
        params = dict(params)
        for key, type_def in definition.items():
            value = params.pop(key, None)
            required = type_def.pop("required", False)
            try:
                print_key = f"{parent}.{key}" if parent else key
                if is_non_empty_value(value):
                    validated_params[key] = self.parse_value(print_key, value, **type_def)
                elif required:
                    print(f"{print_key} should not be empty")
                    raise HTTPInvalidParams()
            finally:
                type_def["required"] = required
        if self.is_strict and is_non_empty_value(params):
            print(f'Unexpected params {list(params.keys())}')
            raise HTTPInvalidParams()
        return validated_params

    def parse_value(self, key, value, data_type, min_val=None, max_val=None, allowed_value_list=None, regex=None,
                    nested=False, sub_item_data_type=None, nested_data_definition=None):
        try:
            value = self.type_converter(value, data_type)
        except Exception:
            print(f"{key} should be of type {data_type}")
            raise HTTPInvalidParams()

        if nested:
            if sub_item_data_type and isinstance(value, list):
                for i, item in enumerate(value):
                    try:
                        list_item = self.type_converter(item, sub_item_data_type)
                        value[i] = list_item
                    except Exception:
                        print(f"{key} should be of {data_type} of {sub_item_data_type}")
                        raise HTTPInvalidParams()
                    self.check_value_constraint(list_item, key, min_val, max_val, allowed_value_list, regex)
            elif nested_data_definition:
                if data_type is dict:
                    value = self.parser(value, nested_data_definition, key)
                elif data_type is list:
                    temp_list = []
                    for item in value:
                        list_item = self.parser(item, nested_data_definition, key)
                        temp_list.append(list_item)
                    value = temp_list
        else:
            self.check_value_constraint(value, key, min_val, max_val, allowed_value_list, regex)
        return value

    @staticmethod
    def check_value_constraint(value, key, min_val=None, max_val=None, allowed_value_list=None, regex=None):
        if min_val and value < min_val:
            print(f"{key} should be greater than or equal to {min_val}")
            raise HTTPInvalidParams()
        if max_val and value > max_val:
            print(f"{key} should be lesser than or equal to {max_val}")
            raise HTTPInvalidParams()
        if allowed_value_list and value not in allowed_value_list:
            print(f"{key} should be one of these - {allowed_value_list}")
            raise HTTPInvalidParams()
        if regex and re.search(regex, value) is None:
            print(f"{key} should be of format - {regex}")
            raise HTTPInvalidParams()

    @staticmethod
    def validate_type_definition(type_definition):
        return type_definition

    @staticmethod
    def get_normalize_query_params():
        params_non_flat = request.args.to_dict(flat=False)
        return {key: value if len(value) > 1 else value[0] for key, value in params_non_flat.items()}

    @staticmethod
    def type_converter(value, data_type):
        if isinstance(data_type, BaseParam) and isinstance(value, data_type.data_type) is False:
            value = data_type(value)
        elif isinstance(value, data_type) is False:
            value = data_type(value)
        return value


def parse_request(json_definition, is_strict=True):
    def inner_get_fu(fu):
        return ParamValidator(json_definition, is_strict=is_strict)(fu)

    return inner_get_fu


class BaseParam:
    def __init__(self, data_type):
        self.data_type = data_type

    def __call__(self, value):
        raise NotImplemented

    def __repr__(self):
        return str(self.data_type)


class DateTimeParam(BaseParam):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=datetime)

    def __call__(self, value):
        if value is None:
            return datetime.now()
        return datetime.strptime(value, self.fmt_string)

    def __repr__(self):
        return f"{self.data_type} and format {self.fmt_string}"


class DateParam(BaseParam):
    def __init__(self, fmt_string):
        self.fmt_string = fmt_string
        super().__init__(data_type=date)

    def __call__(self, value=None):
        if value is None:
            return date.today()
        return datetime.strptime(value, self.fmt_string).date()

    def __repr__(self):
        return f"{str(self.data_type)} and format {self.fmt_string}"


class DecimalParam(BaseParam):
    def __init__(self):
        super().__init__(data_type=Decimal)

    def __call__(self, value=None):
        if value is None:
            return Decimal(0)
        return Decimal(str(value))
