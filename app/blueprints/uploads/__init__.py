from flask import Blueprint, render_template, abort, request, session, jsonify, redirect, url_for
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
    file = request.files["file"]
    if file.filename != "":
        try:
            file.save(os.path.join(os.path.abspath("./app/static/uploads/image/"), file.filename))
            return redirect(url_for('admin.panel')+"?tab=uploadImage")
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
