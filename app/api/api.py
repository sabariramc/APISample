#!/usr/bin/python3
"""
Project : 
Author : sabariram
Date : 02-Aug-2020
"""

from flask import Blueprint
from flask_restful import Api
from .exception.httpexception import HTTPException
from .billdetail import BillDetail
from .paymentupdate import PaymentUpdate


class EventAPI(Api):

    def handle_error(self, e):
        if isinstance(e, HTTPException):
            return {"status": "ERROR",
                    "errorCode": e.message}, e.code
        else:
            return super().handle_error(e)


api = EventAPI()
api.add_resource(BillDetail, "/fetch-bill")
api.add_resource(PaymentUpdate, "/payment-update")

bp = Blueprint("API", __name__)
api.init_app(bp)
