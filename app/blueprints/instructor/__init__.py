from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
)
import os
from app.authorizer import authorize_with

instructor = Blueprint("instructor", __name__, template_folder="templates")


@instructor.before_request
@authorize_with(["canAccessInstructorPanel"])
def middleware():
    pass


@instructor.route("/courseList")
def courseList():
    return render_template(
        "courseList.html",
        isInstructor=True,
        isDLTC=False,
        imagesUrl=[
            url_for(
                "static",
                filename=current_app.config["upload_image_directory"].replace("\\", "/")
                + "/"
                + f,
            )
            for f in os.listdir(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                )
            )
            if os.path.isfile(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                    f,
                )
            )
        ],
    )


@instructor.route("/versionTree/", defaults={"courseCode": None})
@instructor.route("/versionTree/<courseCode>")
def versionTree(courseCode):
    if courseCode is not None:
        return render_template(
            "collegue/versionTree.html",
            courseCode=courseCode,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)


@instructor.route("/courseSchedule/", defaults={"courseCode": None})
@instructor.route("/courseSchedule/<courseCode>")
def courseSchedule(courseCode):
    if courseCode is not None:
        return render_template("instructor/courseSchedule.html", courseCode=courseCode)
    abort(404)


@instructor.route("/material/", defaults={"courseCode": None})
@instructor.route("/material/<courseCode>")
def material(courseCode):
    if courseCode is not None:
        return render_template("instructor/material.html", courseCode=courseCode)
    abort(404)


@instructor.route("/schedule")
def schedule():
    return render_template("courseList.html", isInstructor=True, isDLTC=False)


@instructor.route("/workspace/", defaults={"deltaGraphId": None})
@instructor.route("/workspace/<deltaGraphId>")
def workspace(deltaGraphId):
    if deltaGraphId is not None:
        return render_template("instructor/graphEditor.html", deltaGraphId=deltaGraphId)
    abort(404)


@instructor.route(
    "/workspace/commit/", defaults={"overwriterId": None, "overwriteeId": None}
)
@instructor.route("/workspace/commit/<overwriterId>/", defaults={"overwriteeId": None})
@instructor.route("/workspace/commit/<overwriterId>/<overwriteeId>")
def commit(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)


@instructor.route("/branch/", defaults={"overwriterId": None, "overwriteeId": None})
@instructor.route("/branch/<overwriterId>/", defaults={"overwriteeId": None})
@instructor.route("/branch/<overwriterId>/<overwriteeId>")
def branch(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)


@instructor.route("/import/", defaults={"deltaGraphId": None})
@instructor.route("/import/<deltaGraphId>/")
def graphimport(deltaGraphId):
    if deltaGraphId is not None:
        return render_template("instructor/graphImport.html", deltaGraphId=deltaGraphId)
    abort(404)


@instructor.route("/courseCreate")
def courseForm():
    return render_template(
        "instructor/courseForm.html",
        imagesUrl=[
            url_for(
                "static",
                filename=current_app.config["upload_image_directory"].replace("\\", "/")
                + "/"
                + f,
            )
            for f in os.listdir(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                )
            )
            if os.path.isfile(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                    f,
                )
            )
        ],
    )


@instructor.route("/upload")
def uploadImage():
    return render_template("instructor/uploadImage.html")


@instructor.route("/repositories/", defaults={"courseCode": None})
@instructor.route("/repositories/<courseCode>")
def repositories(courseCode):
    return render_template("instructor/repository.html", courseCode=courseCode)


@instructor.route("/repositories/<courseCode>/versions/", defaults={"id": None})
@instructor.route("/repositories/<courseCode>/versions/<id>")
def repositoryVersions(courseCode, id):
    return render_template(
        "instructor/repositoryVersions.html", courseCode=courseCode, id=id
    )


@instructor.route("/metagraph")
def metagraph():
    return render_template("instructor/metagraph.html")
