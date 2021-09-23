from flask import jsonify, make_response

def success(message):
    res = {
        'message': message
    }

    return make_response(jsonify(res)), 200

def successWithData(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res)), 200

def badRequest(values, message):
    res = {
        'data': values,
        'message': message
    }

    return make_response(jsonify(res)), 400

def NotFound(message):
    res = {
        'message': message
    }

    return make_response(jsonify(res)), 404

def Unauthorized(message):
    res = {
        'message': message
    }

    return make_response(jsonify(res)), 401