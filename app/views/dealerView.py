from sre_constants import FAILURE, SUCCESS
from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (MISSING_FIELD, DEALER_EXISTS,DEALER_ADD_SUCCESS,DEALER_NOT_FOUND, DEALER_UPDATE_SUCCESS, DEALER_DELETE_SUCCESS,MISSING_STATE_TAX, SUCCESS_MSG, FAILURE_MSG)
from app.models.dealerModel import DealerModel
from app.models.stateTaxModel import StateTaxModel

dealer_api = Blueprint("dealer_api", __name__)

@dealer_api.route("/dealer", methods=["POST"])
def add_dealer():
    try:
        req_data = request.get_json()
        check_fields = ["name", "web_url", "street_address", "postal_code", "city", "state"]
        if not validateReqBody(check_fields, req_data):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)

        if "state_tax_id" not in req_data:
            state_tax_id = StateTaxModel.get_state_tax(req_data.get("state"))
            if not state_tax_id:
                return create_response(FAILURE_MSG, MISSING_STATE_TAX, 400 )
            req_data["state_tax_id"] = state_tax_id.get("state_tax_id")

        name = req_data.get("name")
        web_url = req_data.get("web_url")
        if DealerModel.get_dealer_by_name_url(name, web_url):
            return create_response(FAILURE_MSG, DEALER_EXISTS, 400)
        DealerModel.add_dealer(req_data)
        return create_response(SUCCESS_MSG, DEALER_ADD_SUCCESS, 200 )

    except Exception as e:
        print(f"Error while creating dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_api.route("/dealer", methods=["GET"])
def get_dealer():
    try:
        dealer_objs = DealerModel.get_all_dealers()
        return create_response(SUCCESS_MSG, dealer_objs, 200)
    except Exception as e:
        print(f"Error while retrieving dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_api.route("/dealer/<int:dealer_id>", methods=["GET"])
def get_dealer_by_id(dealer_id=None):
    try:
        dealer_obj = DealerModel.get_dealer_by_id(dealer_id)
        return create_response(SUCCESS_MSG, dealer_obj, 200)
    except Exception as e:
        print(f"Error while retrieving dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_api.route("/dealer/state/<state>", methods=["GET"])
def get_dealer_state(state=None):
    try:
        print(state)
        dealer_objs = DealerModel.get_dealers_by_state(state)
        return create_response(SUCCESS_MSG, dealer_objs, 200)
    except Exception as e:
        print(f"Error while retrieving dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)



@dealer_api.route("/dealer/<dealer_id>", methods=["PATCH"])
def update_dealer(dealer_id):
    try:
        req_data = request.get_json()
        update_status = DealerModel.update_dealer(dealer_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, DEALER_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, DEALER_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while updating dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@dealer_api.route("/dealer/<dealer_id>", methods=["DELETE"])
def delete_dealer(dealer_id):
    try:
        delete_status = DealerModel.delete_dealer(dealer_id)
        if not delete_status:
            return create_response(FAILURE_MSG, DEALER_NOT_FOUND, 400)
        return create_response(SUCCESS_MSG, DEALER_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting dealer object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)