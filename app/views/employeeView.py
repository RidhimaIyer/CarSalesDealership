from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (EMPLOYEE_ADD_SUCCESS, EMPLOYEE_NOT_FOUND, EMPLOYEE_UPDATE_SUCCESS, EMPLOYEE_DELETE_SUCCESS, MISSING_FIELD, SUCCESS_MSG, FAILURE_MSG)
from app.models.employeeModel import EmployeeModel
from app.models.dealerModel import DealerModel

employee_api = Blueprint("employee_api", __name__)

@employee_api.route("/employee", methods=["POST"])
def add_employee():
    try:
        req_data = request.get_json()
        check_fields = ["first_name", "last_name", "dealer_id"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        EmployeeModel.add_employee(req_data)
        return create_response(SUCCESS_MSG, EMPLOYEE_ADD_SUCCESS, 200)

    except Exception as e:
        print(f"Error while creating Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@employee_api.route("/employee", methods=["GET"])
def get_employee():
    try:
        employee_objs = EmployeeModel.get_all_employees()
        return create_response(SUCCESS_MSG, employee_objs, 200)
    except Exception as e:
        print(f"Error while creating Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@employee_api.route("/employee/<int:employee_id>", methods=["GET"])
def get_employee_by_id(employee_id):
    try:
        employee_objs = EmployeeModel.get_employee_by_id(employee_id)
        return create_response(SUCCESS_MSG, employee_objs, 200)
    except Exception as e:
        print(f"Error while creating Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@employee_api.route("/employee/dealer/<int:dealer_id>", methods=["GET"])
def get_employee_by_dealer(dealer_id):
    try:
        employee_objs = EmployeeModel.get_employee_by_dealer(dealer_id)
        return create_response(SUCCESS_MSG, employee_objs, 200)
    except Exception as e:
        print(f"Error while creating Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)



@employee_api.route("/employee/<int:employee_id>", methods=["PATCH"])
def update_employee(employee_id=None):
    try:
        req_data = request.get_json()
        update_status = EmployeeModel.update_employee(employee_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, EMPLOYEE_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, EMPLOYEE_UPDATE_SUCCESS, 200)

    except Exception as e:
        print(f"Error while updating Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@employee_api.route("/employee/<int:employee_id>", methods=["DELETE"])
def delete_employee(employee_id=None, dealer_id=None):
    try:
        delete_status = EmployeeModel.delete_employee(employee_id)
        if not delete_status:
            return create_response(FAILURE_MSG, EMPLOYEE_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, EMPLOYEE_DELETE_SUCCESS, 200)

    except Exception as e:
        print(f"Error while deleting Employee object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

