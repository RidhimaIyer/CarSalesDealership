from sre_constants import SUCCESS
from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (MISSING_FIELD,INVENTORY_CAR_DEALER_EXISTS, INVENTORY_ADD_SUCCESS,INVENTORY_CAR_SERIAL_NO_NOT_FOUND, INVENTORY_DEALER_NOT_FOUND, INVENTORY_DEALER_CAR_NOT_FOUND,INVENTORY_UPDATE_SUCCESS, INVENTORY_DELETE_SUCCESS, FAILURE_MSG, SUCCESS_MSG )
from app.models.dealerInventoryModel import DealerInventoryModel

dealer_inventory_api = Blueprint("dealer_inventory_api", __name__)

@dealer_inventory_api.route("/dealer_inventory", methods=["POST"])
def add_dealer_inventory():
    try:
        req_data = request.get_json()
        check_fields = ["car_serial_no", "dealer_id", "car_count"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)

        car_serial_no = req_data.get("car_serial_no")
        dealer_id = req_data.get("dealer_id")
        if DealerInventoryModel.car_dealer_record_exists(car_serial_no, dealer_id):
            return create_response(FAILURE_MSG, INVENTORY_CAR_DEALER_EXISTS, 400)

        DealerInventoryModel.add_dealer_inventory(req_data)
        return create_response(SUCCESS_MSG, INVENTORY_ADD_SUCCESS, 200)
    except Exception as e:
        print(f"Error while creating dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_inventory_api.route("/dealer_inventory", methods=["GET"])
def get_dealer_inventory():
    try:
        inventory_objs = DealerInventoryModel.get_all_inventory()
        return create_response(SUCCESS_MSG, inventory_objs,200)
    except Exception as e:
        print(f"Error while retrieving dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_inventory_api.route("/dealer_inventory/<int:dealer_id>", methods=["GET"])
def get_dealer_inventory_by_dealer_id(dealer_id):
    try:
        inventory_objs = DealerInventoryModel.get_inventory_by_dealer(dealer_id)
        if not inventory_objs:
            return create_response(FAILURE_MSG, INVENTORY_DEALER_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, inventory_objs, 200)
    except Exception as e:
        print(f"Error while retrieving dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_inventory_api.route("/dealer_inventory/<int:dealer_id>/<int:car_serial_no>", methods=["GET"])
def get_dealer_inventory_by_dealer_car(dealer_id, car_serial_no):
    try:
        inventory_obj = DealerInventoryModel.get_inventory_by_dealer_car(dealer_id, car_serial_no)
        if not inventory_obj:
            return create_response(FAILURE_MSG, INVENTORY_CAR_SERIAL_NO_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, inventory_obj, 200)
    except Exception as e:
        print(f"Error while retrieving dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_inventory_api.route("/dealer_inventory/<int:dealer_id>/<int:car_serial_no>", methods=["PATCH"])
def update_dealer_inventory(dealer_id, car_serial_no):
    try:
        req_data = request.get_json()
        print(req_data)
        update_status = DealerInventoryModel.update_dealer_inventory_count(dealer_id, car_serial_no, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, INVENTORY_DEALER_CAR_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, INVENTORY_UPDATE_SUCCESS, 200 )
    except Exception as e:
        print(f"Error while updating dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_inventory_api.route("/dealer_inventory/<int:dealer_id>/<int:car_serial_no>", methods=["DELETE"])
def delete_inventory(dealer_id, car_serial_no):
    try:
        delete_status = DealerInventoryModel.delete_dealer_inventory(dealer_id, car_serial_no)
        if not delete_status:
            return create_response(FAILURE_MSG, INVENTORY_DEALER_CAR_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, INVENTORY_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting dealer inventory record")
        return create_response(FAILURE_MSG, str(e), 500)





        



