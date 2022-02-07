from flask import Blueprint, render_template, session, redirect, abort

collaborate = Blueprint("collaborate", __name__, template_folder="templates")
from app.authorizer import authorize_with


@collaborate.route("/graphEditing")
@authorize_with(["canProposeRelationship"])
def graphEditing():
    return render_template("collaborate/graphEditing.html")


@collaborate.route("/feedbacks")
@authorize_with([["canGiveFeedback", "canReplyFeedback"]])
def feedbacks():
    return render_template("shared/courseList.html")


@collaborate.route("/feedbacks/<courseCode>")
@authorize_with([["canGiveFeedback", "canReplyFeedback"]])
def courseFeedbacks(courseCode):
    return render_template("collaborate/feedback.html", courseCode=courseCode)


@collaborate.route("/post", defaults={"id": None})
@collaborate.route("/post/<id>")
@authorize_with([["canGiveFeedback", "canReplyFeedback"]])
def post(id):
    if id is not None:
        return render_template("collaborate/post.html", id=id)


@collaborate.route("/metagraph")
@authorize_with([], True, roles=["DLTC", "instructor", "admin", "operator"])
def metagraph():
    return render_template("collaborate/metagraph.html")
