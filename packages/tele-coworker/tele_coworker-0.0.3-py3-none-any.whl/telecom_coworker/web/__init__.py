from flask import jsonify


def ok(data=None):
    data = data if data else {}

    return jsonify({
        'code': 0,
        'payload': data
    }), 200


def fail(code, error_message):
    return jsonify({
        'code': code,
        'message': error_message
    }), 200
