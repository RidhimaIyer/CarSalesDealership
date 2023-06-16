from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (CUSTOMER_DELETE_SUCCESS, MISSING_FIELD, CUSTOMER_EMAIL_EXISTS,CUSTOMER_ADD_SUCCESS,CUSTOMER_ID_NOT_FOUND, CUSTOMER_EMAIL_NOT_FOUND,CUSTOMER_UPDATE_SUCCESS, SUCCESS_MSG, FAILURE_MSG)
from app.models.customerModel import CustomerModel

customer_api = Blueprint("customer_api", __name__)

@customer_api.route("/customer", methods=["POST"])
def add_customer():
    try:
        req_data = request.get_json()
        check_fields = ["phone", "email_id", "ssn", "first_name", "last_name", "address"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        email_id = req_data.get("email_id")
        if CustomerModel.get_customer_by_email(email_id):
            return create_response(FAILURE_MSG, CUSTOMER_EMAIL_EXISTS, 400)

        CustomerModel.add_customer(req_data)
        return create_response(SUCCESS_MSG, CUSTOMER_ADD_SUCCESS, 200)

    except Exception as e:
        print(f"Error while creating customer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@customer_api.route("/customer", methods=["GET"])
def get_customer():
    try:
            customer_objs = CustomerModel.get_all_customers()
            return create_response(SUCCESS_MSG, customer_objs, 200)
    except Exception as e:
        print(f"Error while retrieving customer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@customer_api.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_by_id(customer_id=None):
    try:
        customer_obj = CustomerModel.get_customer_by_id(customer_id)
        if not customer_obj:
            return create_response(FAILURE_MSG, CUSTOMER_ID_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, customer_obj, 200)
    except Exception as e:
        print(f"Error while retrieving customer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@customer_api.route("/customer/<int:customer_id>", methods=["PATCH"])
def update_customer(customer_id):
    try:
        req_data = request.get_json()
        update_status = CustomerModel.update_customer_record(customer_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, CUSTOMER_ID_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, CUSTOMER_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while updating customer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@customer_api.route("/customer/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    try:
        delete_status = CustomerModel.delete_customer(customer_id)
        if not delete_status:
            return create_response(FAILURE_MSG, CUSTOMER_ID_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, CUSTOMER_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting customer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

    