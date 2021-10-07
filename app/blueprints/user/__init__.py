from flask import Blueprint, render_template, abort, redirect, request
from app.api_driver import get_api_driver

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/")
def back():
    return redirect("/")


@user.route("/profile")
def profile():
    return render_template("user/profile.html")


@user.route("/logout")
def logout():
    return redirect("/")


@user.route("/authenticate")
def authenticate():
    return redirect("/")
