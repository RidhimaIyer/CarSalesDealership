from datetime import datetime, timedelta
from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (MISSING_FIELD, SALE_ADDED_SUCCCESS,SALE_INVOICE_IF_NOT_FOUND, SALE_UPDATE_SUCCESS, SALE_DELETE_SUCCESS,  SUCCESS_MSG, FAILURE_MSG)
from app.models.saleModel import SaleModel

sale_api = Blueprint("sale_api", __name__)

@sale_api.route("/sale", methods=["POST"])
def add_invoice():
    try:
        req_data = request.get_json()
        check_fields = ["date_of_purchase", "dealer_id", "customer_id", "employee_id" ]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        req_data["date_of_purchase"] = datetime.strptime(req_data["date_of_purchase"], "%Y-%m-%d")

        SaleModel.add_invoice(req_data)
        return create_response(SUCCESS_MSG, SALE_ADDED_SUCCCESS, 200)
    except Exception as e:
        print(f"Error while creating sale object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_api.route("/sale/<int:dealer_id>", methods=["GET"])
def get_sale_by_date(dealer_id):
    try:

        start_dt = request.args.get("start_dt") 
        end_dt = request.args.get("end_dt")
        
        start_dt = datetime.strptime(start_dt, "%Y-%m-%d") if start_dt else datetime.utcnow() - timedelta(days=90)
        end_dt = datetime.strptime(end_dt, "%Y-%m-%d") if end_dt else datetime.utcnow()

        sale_objs = SaleModel.get_invoice_by_date(dealer_id, start_dt, end_dt)
        return create_response(SUCCESS_MSG, sale_objs, 200)
    except Exception as e:
        print(f"Error while retrieving sale object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_api.route("/sale/<int:dealer_id>/<int:customer_id>", methods=["GET"])
def get_invoice_by_cust_date(dealer_id, customer_id):
    try:
        start_dt = request.args.get("start_dt") 
        end_dt = request.args.get("end_dt")
        
        start_dt = datetime.strptime(start_dt, "%Y-%m-%d") if start_dt else datetime.utcnow() - timedelta(days=90)
        end_dt = datetime.strptime(end_dt, "%Y-%m-%d") if end_dt else datetime.utcnow()


        sale_objs = SaleModel.get_invoice_by_cust_date(dealer_id, customer_id, start_dt, end_dt)
        return create_response(SUCCESS_MSG, sale_objs, 200)
    except Exception as e:
        print(f"Error while retrieving sale object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_api.route("/sale/<invoice_id>", methods=["PATCH"])
def update_sale_record(invoice_id):
    try:
        req_data = request.get_json()
        update_status = SaleModel.update_invoice(invoice_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, SALE_INVOICE_IF_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, SALE_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while updating sale object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_api.route("/sale/<invoice_id>", methods=["DELETE"])
def delete_sale_record(invoice_id):
    try:
        delete_status = SaleModel.delete_invoice(invoice_id)
        if not delete_status:
            return create_response(FAILURE_MSG, SALE_INVOICE_IF_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, SALE_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting sale object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)




    
    
