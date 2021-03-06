#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from flask_restful import Resource

from .requestparser import parse_request, requires_api_key

from ..db import execute_query

from .exception import HTTPCustomerNotFound

from ..utility import is_non_empty_value


class BillDetail(Resource):

    @parse_request({
        "mobileNumber": {'data_type': str, 'required': True, 'regex': r'^[6-9]\d{9}$'}
    }
    )
    def post(self, mobileNumber):
        user_data = execute_query(
            "SELECT * FROM customer cu LEFT OUTER JOIN customer_due cd ON cd.customer_id = cu.id WHERE cu.mobile_number = ?",
            (mobileNumber,))
        if len(user_data) == 0:
            raise HTTPCustomerNotFound()
        user_data = user_data[0]
        due_amount = user_data.get('due_amount')
        due_amount = due_amount if is_non_empty_value(due_amount) else 0
        due_amount = due_amount if due_amount > 0 else 0
        response_data = {
            "customerName": user_data.get('name'),
        }
        if due_amount > 0:
            paid_amount = user_data.get('paid_amount')
            due_amount = due_amount - paid_amount if is_non_empty_value(paid_amount) else due_amount
            response_data['dueAmount'] = str(due_amount)
            if due_amount > 0:
                response_data['dueDate'] = user_data.get('due_date')
                response_data['refID'] = user_data.get('reference_id')
        return response_data
