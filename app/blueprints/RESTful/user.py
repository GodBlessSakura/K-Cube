from flask import request
from app.api_driver import get_api_driver
from . import RESTful

@RESTful.route('/check-unused-userId', methods = ['GET'])
def checkUnusedUserId():
    userId = request.args['userId']
    return str(not get_api_driver().user.is_userId_used(userId))