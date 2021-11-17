from flask import Blueprint, render_template, session, redirect, abort

collaborate = Blueprint("collaborate", __name__, template_folder="templates")
from app.authorizer import authorize_with


@collaborate.route("/relationships")
@authorize_with(["canProposeRelationship"])
def relationships():
    return render_template("collaborate/index.html")


@collaborate.route("/feedbacks")
@authorize_with(["canProposeRelationship"])
def feedbacks():
    return render_template(
        "collegue/courseList.html",
        isInstructor=False,
        isDLTC=False,
        isFeedback=True,
    )


@collaborate.route("/feedbacks/<courseCode>")
@authorize_with(["canProposeRelationship"])
def courseFeedbacks(courseCode):
    return render_template("collaborate/feedback.html", courseCode=courseCode)


@collaborate.route("/post", defaults={"id": None})
@collaborate.route("/post/<id>")
@authorize_with(["canProposeRelationship"])
def post(id):
    if id is not None:
        return render_template("collaborate/post.html", id=id)
