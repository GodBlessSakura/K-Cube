from flask_socketio import SocketIO, emit, join_room


def setup_socketio(app):
    socketio = SocketIO(app)


    @socketio.on("graphEditor-joinRoom")
    def roomResolve(deltaGraphId):
        #check if user have edit permission
        join_room("graphEditor-" + deltaGraphId)


    socketio.run(app)
