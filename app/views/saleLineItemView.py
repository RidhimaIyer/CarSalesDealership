from flask import Blueprint, request
from app.models.dealerModel import DealerModel
from helper import create_response, validateReqBody
from resp_messages import (CAR_SERIAL_NOT_FOUND,DEALER_NOT_FOUND,MISSING_FIELD,SALE_ITEM_ADDED_SUCCESS,SALE_ITEM_INVOICE_NOT_FOUND, SALE_ITEM_UPDATE_SUCCESS, SALE_ITEM_DELETE_SUCCESS,  SUCCESS_MSG, FAILURE_MSG)
from app.models.saleLineItemModel import SaleLineItemModel
from app.models.carModel import CarModel
from app.models.dealerModel import DealerModel
from app.models.stateTaxModel import StateTaxModel
from app.models.saleModel import SaleModel

sale_line_item_api = Blueprint("sale_line_item_api", __name__)

def update_sale_invoice_price(invoice_id):
    sale_item_objs = SaleLineItemModel.get_sale_line_item_by_invoice(invoice_id)
    total_invoice_amt = 0 
    total_tax_amt = 0 
    for item in sale_item_objs:
        total_invoice_amt += item.get("car_net_price")
        total_tax_amt += item.get("item_tax")
    sale_price_update_req = {
            "net_price": float(total_invoice_amt),
            "net_tax": float(total_tax_amt)
        }

    SaleModel.update_invoice(invoice_id, sale_price_update_req )


@sale_line_item_api.route("/sale_item", methods=["POST"])
def add_sale_line_item():
    try:

        req_data = request.get_json()
        check_fields= ["invoice_id","dealer_id", "cart"]
        if not validateReqBody(req_data, check_fields):
            return create_response(FAILURE_MSG, MISSING_FIELD, 400)
        
        check_fields = ["car_serial_no"]
        for item in req_data.get("cart"):
            if not validateReqBody(item, check_fields):
                return create_response(FAILURE_MSG, MISSING_FIELD, 400)
            if "car_unit_price" not in item:
                try:
                    item["car_unit_price"] = CarModel.get_car_by_serial(item.get("car_serial_no")).get("price")
                except Exception as e:
                    return create_response(FAILURE_MSG, CAR_SERIAL_NOT_FOUND, 400)
            if "state_tax" not in item:
                try:
                    state_tax_id = DealerModel.get_dealer_by_id(req_data.get("dealer_id")).get("state_tax_id")
                    item["state_tax"] = StateTaxModel.get_state_by_id(state_tax_id)["tax"]
                except Exception as e:
                    return create_response(FAILURE_MSG, DEALER_NOT_FOUND, 400)

        SaleLineItemModel.add_invoice_line_item(req_data)
        invoice_id = req_data.get("invoice_id")
        update_sale_invoice_price(invoice_id)
        return create_response(SUCCESS_MSG, SALE_ITEM_ADDED_SUCCESS, 200)
    
    except Exception as e:
        print(f"Error while creating sale item object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_line_item_api.route("/sale_item/<int:invoice_id>", methods=["GET"])
def get_sale_item(invoice_id):
    try:
        sale_item_objs = SaleLineItemModel.get_sale_line_item_by_invoice(invoice_id)
        return create_response(SUCCESS_MSG, sale_item_objs, 200)
    except Exception as e:
        print(f"Error while retrieving sale item object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_line_item_api.route("/sale_item/<int:invoice_line_item_id>", methods=["PATCH"])
def update_sale_item(invoice_line_item_id):
    try:
        req_data = request.get_json()
        update_status, invoice_id = SaleLineItemModel.update_sale_line(invoice_line_item_id, req_data)
        if not update_status:
            return create_response(FAILURE_MSG, SALE_ITEM_INVOICE_NOT_FOUND, 400)

        update_sale_invoice_price(invoice_id)
        return create_response(SUCCESS_MSG, SALE_ITEM_UPDATE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while updating sale line item object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)

@sale_line_item_api.route("/sale_item/<int:invoice_line_item_id>", methods=["DELETE"])
def delete_sale_item(invoice_line_item_id):
    try:

        delete_status, invoice_id = SaleLineItemModel.delete_sale_line(invoice_line_item_id)
        if not delete_status:
            return create_response(FAILURE_MSG, SALE_ITEM_INVOICE_NOT_FOUND, 400)
        update_sale_invoice_price(invoice_id)
        return create_response(SUCCESS_MSG, SALE_ITEM_DELETE_SUCCESS, 200)
    except Exception as e:
        print(f"Error while deleting sale line item object:{e}")
        return create_response(FAILURE_MSG, str(e), 500)
