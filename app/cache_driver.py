from flask_caching import Cache


cache = Cache(config={"CACHE_TYPE": "SimpleCache"})


@cache.memoize()
def user_permission(userId):
    from app.api_driver import get_api_driver

    return get_api_driver().user.get_user_permission(userId=userId)


@cache.memoize()
def user_info(userId):
    from app.api_driver import get_api_driver

    return get_api_driver().user.get_user(userId=userId)
