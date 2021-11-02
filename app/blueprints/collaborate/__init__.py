from flask import Blueprint, render_template, session, redirect, abort

collaborate = Blueprint("collaborate", __name__, template_folder="templates")
from app.authorizer import authorize_with


@collaborate.route("/")
@authorize_with(["canProposeRelationship"])
def index():
    return render_template("collaborate/index.html")
