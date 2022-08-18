from tkinter.font import names
from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
    g,
)
import os
from app.authorizer import authorize_with
from app.blueprints.collaborate import collaborate

instructor = Blueprint("instructor", __name__, template_folder="templates")


@instructor.route("/dashboard")
def dashboard():
    return render_template(
        "instructor/dashboard.html",
        components=[
            "/".join([instructor.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    instructor.root_path,
                    instructor.template_folder,
                    instructor.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    instructor.root_path,
                    instructor.template_folder,
                    instructor.name,
                    "dashboardComponents",
                    f,
                )
            )
        ]
        + [
            "/".join([collaborate.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                    f,
                )
            )
        ],
    )


@instructor.before_request
@authorize_with([], True, ["instructor", "admin"])
def middleware():
    pass


@instructor.route("/courseList")
def courseList():
    return render_template(
        "shared/courseList.html",
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
        )
    abort(404)


@instructor.route("/coursePlan/", defaults={"courseCode": None})
@instructor.route("/coursePlan/<courseCode>")
def coursePlan(courseCode):
    if courseCode is not None:
        return render_template(
            "shared/coursePlan/coursePlan.html", courseCode=courseCode
        )
    abort(404)


@instructor.route("/material/", defaults={"courseCode": None})
@instructor.route("/material/<courseCode>")
def material(courseCode):
    if courseCode is not None:
        return render_template("instructor/material.html", courseCode=courseCode)
    abort(404)


@instructor.route("/schedule")
def schedule():
    return "not implemented"


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


@instructor.route("/disambiguation", defaults={"courseCode": None})
@instructor.route("/disambiguation/<courseCode>")
def disambiguation(courseCode):
    from app.api_driver import get_api_driver

    return render_template(
        "instructor/disambiguation.html",
        courseCode=courseCode if courseCode is not None else "",
        courseCodes=[
            c["concept"]["name"]
            for c in get_api_driver().course.list_internal_course(
                userId=g.user["userId"]
            )
        ],
        names=[e["concept"]["name"] for e in get_api_driver().entity.list_entity()],
    )


@instructor.route("/entityEditor", defaults={"courseCode": None, "name": None})
@instructor.route("/entityEditor/<courseCode>/", defaults={"name": None})
@instructor.route("/entityEditor/<courseCode>/<path:name>")
def entityEditor(courseCode, name):
    from app.api_driver import get_api_driver

    return render_template(
        "instructor/entityEditor.html",
        courseCode=courseCode,
        name=name,
    )
