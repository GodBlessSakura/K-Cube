if __name__ == "__main__":
    from flask_socketio import SocketIO, emit, join_room
    from flask import g
    from app import create_app
    from functools import wraps
    import os
    import argparse

    # 构造命令行参数并根据命令函参数在config.py文件下选择相应的配置选项
    parser = argparse.ArgumentParser()
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("--mode", type=str, default="development")
    args = parser.parse_args()

    app = create_app(args.mode)

    # 学习下socketio的用法 0703
    socketio = SocketIO(app , cors_allowed_origins="*") #cors_allowed_origins表示允许跨域请求

    def load_info_from_cache(function):
        @wraps(function)  # 使用__name__时打印被装饰的函数而不是装饰器内部的函数
        def wrapper(*args, **kwargs):
            from app.cache_driver import load_info_from_cache

            load_info_from_cache()
            return function(*args, **kwargs)

        return wrapper

    @socketio.on("start", namespace="/graphEditor") # 监听到start事件就开始执行下面的start函数，但是好像没有使用，没有找到正在使用的socket.emit(start)事件
    @load_info_from_cache
    def start(deltaGraphId):
        # check if user have edit permission
        from app.api_driver import get_api_driver

        if get_api_driver().workspace.is_coauthor_or_owner(
            deltaGraphId=deltaGraphId,
            userId=g.user["userId"],
        ):
            join_room(deltaGraphId)
            workspace = get_api_driver().workspace.get_workspace(
                deltaGraphId=deltaGraphId, userId=g.user["userId"]
            )
            join_room(workspace["owner"]["userId"] + "-" + workspace["course"]["name"])
            join_room(workspace["course"]["name"])
            emit(
                "workspaceData",
                {
                    "success": True,
                    "workspace": workspace,
                    "triples": get_api_driver().triple.get_workspace_triple(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                    "subject": get_api_driver().workspace.get_workspace_subject(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                    "subject_triples": get_api_driver().triple.get_workspace_subject_triple(
                        deltaGraphId=deltaGraphId, userId=g.user["userId"]
                    ),
                },
            )
        else:
            emit("workspaceData", {"success": False})

    @socketio.event(namespace="/graphEditor")  # 处理自定义事件，当客户端发送名为createWorkspaceTriple的自定义事件时，进入下面的逻辑
    def createWorkspaceTriple(data):
        emit(
            "createWorkspaceTriple",
            data["payload"],
            to=data["workspace"]["deltaGraphId"],
        )

    @socketio.event(namespace="/graphEditor")
    def deleteWorkspaceTriple(data):
        emit(
            "deleteWorkspaceTriple",
            data["payload"],
            to=data["workspace"]["deltaGraphId"],
        )

    @socketio.event(namespace="/graphEditor")
    def exposureToggle(data):
        workspace = data["workspace"]
        emit(
            "exposureToggle",
            data["payload"],
            to=workspace["owner"]["userId"] + "-" + workspace["course"]["name"],
        )

    @socketio.event(namespace="/graphEditor")
    def joinToggle(data):
        workspace = data["workspace"]
        emit(
            "joinToggle",
            data["payload"],
            to=workspace["owner"]["userId"] + "-" + workspace["course"]["name"],
        )

    # It will call eventlet.wsgi.server at
    # https://github.com/miguelgrinberg/Flask-SocketIO/blob/main/src/flask_socketio/__init__.py#L679
    import os
    environ = os.environ
    socketio.run(app, host=args.host, port=args.port, environ=environ, debug=True)
