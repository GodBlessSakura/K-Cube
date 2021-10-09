from flask import Blueprint, render_template, abort
draft = Blueprint('draft',__name__, template_folder='templates')
@draft.route('/')
def my_space():
    return render_template('draft/my_space.html')