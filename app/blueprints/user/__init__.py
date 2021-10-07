from flask import Blueprint, render_template, abort, redirect, request
from app.db import get_db
user = Blueprint('user',__name__, template_folder='templates')
@user.route('/')
def back():
    return redirect('/')

@user.route('/profile')
def profile():
    return render_template('user/profile.html')
    

@user.route('/logout')
def logout():
    return redirect('/')


@user.route('/authenticate')
def authenticate():
    return redirect('/')

@user.route('/check-unused-id/', methods = ['GET'])
def checkUnusedUserId():
    userId = request.args
    return get_db().check_used_userId(userId)