from flask import Blueprint, render_template, abort
comprehensive = Blueprint('comprehensive',__name__, template_folder='templates')
@comprehensive.route('/')
def graph():
    return render_template('comprehensive/graph.html')