from flask import (
    Blueprint,
    render_template,
    abort,
    request,
    session,
    jsonify,
    redirect,
    url_for,
    current_app,
)
from app import InvalidRequest


uploads = Blueprint(
    "uploads",
    __name__,
)

import os


@uploads.route("/image", methods=["post"])
def image():
    if not session["permission"] or not session["permission"]["canUploadPhoto"]:
        return InvalidRequest("unauthorized operation")
    if "file" not in request.files:
        return jsonify({"success": False, "message": "Form input 'file' is empty"})
    files = request.files.getlist("file")
    try:
        for file in files:
            filename = os.path.split(file.filename)[1]
            if filename != "":
                file.save(
                    os.path.join(
                        current_app.root_path,
                        "static",
                        current_app.config["upload_image_directory"],
                        filename,
                    )
                )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": True})
