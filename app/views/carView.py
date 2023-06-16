from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (MISSING_FIELD, CAR_SERIAL_EXISTS,CAR_SERIAL_NOT_FOUND, CAR_ADD_SUCCESS, CAR_UPDATE_SUCCESS, CAR_DELETE_SUCCESS, SUCCESS_MSG, FAILURE_MSG)
from app.models.carModel import CarModel

car_api = Blueprint("car_api", __name__)


@car_api.route("/car", methods=["POST"])
def add_car():
    try:
        req_data = request.get_json()
        check_fields = ["car_serial_no", "price"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        car_serial_no = req_data.get("car_serial_no")
        if CarModel.get_car_by_serial(car_serial_no):
            return create_response(FAILURE_MSG, CAR_SERIAL_EXISTS, 400)

        CarModel.add_car(req_data)
        return create_response(SUCCESS_MSG, CAR_ADD_SUCCESS, 200)

    except Exception as e:
        print(f"Error while creating car object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@car_api.route("/car", methods=["GET"])
def get_car():
    try:
        car_objs = CarModel.get_all_cars()
        return create_response(SUCCESS_MSG, car_objs, 200)
    except Exception as e:
        print(f"Error while retrieving car objects:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@car_api.route("/car/<car_serial_no>", methods=["GET"])
def get_car_serial_no(car_serial_no):
    try:
        car_obj = CarModel.get_car_by_serial(car_serial_no)
        if not car_obj:
            return create_response(FAILURE_MSG, CAR_SERIAL_NOT_FOUND, 400)
        
        return create_response(SUCCESS_MSG, car_obj, 200)
    except Exception as e:
        print(f"Error while retrieving car objects:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@car_api.route("/car/<car_serial_no>", methods=["PATCH"])
def update_car_record(car_serial_no):
    try:
        req_data = request.get_json()
        check_fields = ["price"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)

        update_status = CarModel.update_car_record(car_serial_no, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, CAR_SERIAL_NOT_FOUND, 400)
        
        return create_response(SUCCESS_MSG, CAR_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while retrieving car objects:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@car_api.route("/car/<car_serial_no>", methods=["DELETE"])
def delete_car(car_serial_no):
    try:
        delete_status = CarModel.delete_car(car_serial_no)
        if not delete_status:
            return create_response(FAILURE_MSG, CAR_SERIAL_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, CAR_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while retrieving car objects:{e}")
        return create_response(FAILURE_MSG, str(e), 500)
    

    

    