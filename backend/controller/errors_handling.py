from flask import jsonify
from . import routes


@routes.errorhandler(404)
def not_found(error):
    return (
        jsonify(
                {
                    "success": False, 
                    "error": 404, 
                    "message": "resource not found"
                }
            ),
        404,
    )


@routes.errorhandler(422)
def unprocessable(error):
    return (
        jsonify(
                {
                    "success": False, 
                    "error": 422, 
                    "message": "unprocessable"
                }
            ),
        422,
    )

@routes.errorhandler(400)
def bad_request(error):
    return (
        jsonify(
                {
                    "success": False, 
                    "error": 400, 
                    "message": "bad request"
                }
            ),
        400,
    )