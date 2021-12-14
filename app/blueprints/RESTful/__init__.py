from flask import Blueprint, render_template, abort

RESTful = Blueprint("RESTful", __name__)

from .courseAPI import course

RESTful.register_blueprint(course)

from .draftAPI import draft

RESTful.register_blueprint(draft)

from .graphAPI import graph

RESTful.register_blueprint(graph)

from .relationshipAPI import relationship

RESTful.register_blueprint(relationship)

from .roleAPI import role

RESTful.register_blueprint(role)

from .tripleAPI import triple

RESTful.register_blueprint(triple)

from .entityAPI import entity

RESTful.register_blueprint(entity)

from .treeAPI import tree

RESTful.register_blueprint(tree)

from .workspaceAPI import workspace

RESTful.register_blueprint(workspace)

from .branchAPI import branch

RESTful.register_blueprint(branch)

from .trunkAPI import trunk

RESTful.register_blueprint(trunk)

from .materialAPI import material

RESTful.register_blueprint(material)

from .feedbackAPI import feedback

RESTful.register_blueprint(feedback)

from .repositoryAPI import repository

RESTful.register_blueprint(repository)
