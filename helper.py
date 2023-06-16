from flask import make_response 

def create_response(status, msg, status_code):
    res = {
        "status": status,
        "msg": msg
    }
    response = make_response(
        res, status_code
    )
    response.headers["Content-Type"] = "application/json"
    return response

def validateReqBody(req_data, check_fields):
    for field in check_fields:
        if field not in req_data:
            return False 
    return True 