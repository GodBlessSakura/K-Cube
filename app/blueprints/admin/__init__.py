from flask import Blueprint, render_template, abort
admin = Blueprint('admin',__name__, template_folder='templates')
@admin.route('/')
def panel():
    return render_template('admin/panel.html')