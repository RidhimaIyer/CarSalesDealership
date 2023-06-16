from flask import Blueprint, request
from helper import create_response, validateReqBody
from resp_messages import (MISSING_FIELD,STATE_TAX_EXISTS,STATE_TAX_ADD_SUCCESS, STATE_TAX_ID_NOT_FOUND, STATE_NOT_FOUND,STATE_TAX_UPDATE_SUCCESS, STATE_TAX_DELETE_SUCCESS,  SUCCESS_MSG, FAILURE_MSG)
from app.models.stateTaxModel import StateTaxModel

state_tax_api = Blueprint("state_tax_api", __name__)

@state_tax_api.route("/state_tax", methods=["POST"])
def add_state_tax():
    try:
        req_data = request.get_json()
        check_fields = ["state", "tax"]
        if not validateReqBody(check_fields, req_data):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        state = req_data.get("state")
        if StateTaxModel.get_state_tax(state):
            return create_response(FAILURE_MSG, STATE_TAX_EXISTS, 400 )
        
        StateTaxModel.add_state_tax(req_data)
        return create_response(SUCCESS_MSG, STATE_TAX_ADD_SUCCESS, 200 )
    except Exception as e:
        print(f"Error while creating state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@state_tax_api.route("/state_tax", methods=["GET"])
def get_all_state_tax():
    try:
        state_tax_objs = StateTaxModel.get_all_state_tax()
        return create_response(SUCCESS_MSG, state_tax_objs, 200)
    except Exception as e:
        print(f"Error while retrieving state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)


@state_tax_api.route("/state_tax/<int:state_tax_id>", methods=["GET"])
def get_state_by_id(state_tax_id):
    try:
        state_tax_objs = StateTaxModel.get_state_by_id(state_tax_id)
        if not state_tax_objs:
            return create_response(FAILURE_MSG, STATE_TAX_ID_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, state_tax_objs, 200)
    except Exception as e:
        print(f"Error while retrieving state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)


@state_tax_api.route("/state_tax/state/<state>", methods=["GET"])
def get_state_tax(state):
    try:
        state_tax_objs = StateTaxModel.get_state_tax(state)
        if not state_tax_objs:
            return create_response(FAILURE_MSG, STATE_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, state_tax_objs, 200)
    except Exception as e:
        print(f"Error while retrieving state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@state_tax_api.route("/state_tax/<state_tax_id>", methods=["PATCH"])
def update_state_tax(state_tax_id = None):
    try:
        req_data = request.get_json()
        update_status = StateTaxModel.update_state_tax(state_tax_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, STATE_TAX_ID_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, STATE_TAX_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while updating state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@state_tax_api.route("/state_tax/<state_tax_id>", methods=["DELETE"])
def delete_state_tax(state_tax_id = None):
    try:
        delete_status = StateTaxModel.delete_state_tax(state_tax_id)
        if not delete_status:
            return create_response(FAILURE_MSG, STATE_TAX_ID_NOT_FOUND, 400 )
        return create_response(SUCCESS_MSG, STATE_TAX_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting state tax object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)