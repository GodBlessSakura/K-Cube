from flask import Blueprint, render_template, abort
uploads = Blueprint('uploads',__name__, static_folder='static')
