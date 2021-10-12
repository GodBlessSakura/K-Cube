from flask import Blueprint, render_template, session, redirect, abort

draft = Blueprint("draft", __name__, template_folder="templates")


@draft.route("/my_space/")
def my_space():
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
        return render_template("draft/my_space.html")
    abort(404)

@draft.route("/my_space/<courseCode>/")
def my_drafts(courseCode):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
        return render_template("draft/my_draft.html", courseCode = courseCode)
    abort(404)

@draft.route("/edit", defaults={"draftId": None})
@draft.route("/edit/<draftId>/")
def edit_draft(draftId):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
        return render_template("draft/graphEditor.html", draftId = draftId)
    abort(404)