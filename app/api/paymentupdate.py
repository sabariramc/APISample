#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from flask_restful import Resource
from time import time

from .requestparser import parse_request, requires_api_key, DateParam
from ..db import execute_query, get_db
from .exception import HTTPInvalidReference, HTTPAmountMisMatch


class PaymentUpdate(Resource):

    @parse_request(
        {
            'refID': {'data_type': str, 'required': True, }
            , 'transaction': {
            'required': True,
            'data_type': dict,
            'nested': True,
            'nested_data_definition': {
                'amountPaid': {'data_type': float, 'required': True, 'min_val': 0}
                , 'date': {'data_type': DateParam('%Y-%m-%d'), 'required': True}
                , 'id': {'data_type': str, 'required': True, }
            }
        }
        }
    )
    def post(self, refID, transaction):
        due_data = execute_query("SELECT * FROM customer_due WHERE reference_id = ?", (refID,))
        if len(due_data) <= 0:
            raise HTTPInvalidReference()
        due_data = due_data[0]
        transaction_data = execute_query("SELECT * FROM due_payment_info WHERE transaction_id = ?",
                                         (transaction.get('id'),))
        if len(transaction_data) <= 0:
            if transaction.get('amountPaid') != due_data.get('due_amount'):
                raise HTTPAmountMisMatch()
            acknowledgement_id = f'ACK{int(time())}'
            db_conn = get_db()
            execute_query(
                "insert into due_payment_info(due_id,amount_paid,paid_on_date,transaction_id,acknowledgement_id)VALUES(?,?,?,?,?)"
                , (due_data.get('id'), transaction.get('amountPaid'), str(transaction.get('date')),
                   transaction.get('id'), acknowledgement_id))
            execute_query(
                "update customer_due set paid_amount = ? where id = ?",
                (due_data.get('due_amount'), due_data.get('id'))
            )
            db_conn.commit()
        else:
            transaction_data = transaction_data[0]
            if transaction_data.get('due_id') != due_data.get('id'):
                raise HTTPInvalidReference()
            acknowledgement_id = transaction_data.get('acknowledgement_id')
        return {
            'ackID': acknowledgement_id
        }
