from oic.oic import Client
from oic.utils.authn.client import CLIENT_AUTHN_METHOD
from flask import current_app, g
from oic import rndstr
from oic.utils.http_util import Redirect
from flask import session


def oidc_args(state=None, nonce=None):
    if state is not None and "oidc_state" not in session:
        session["oidc_state"] = state
    if nonce is not None and "oidc_nonce" not in session:
        session["oidc_nonce"] = nonce
    return {
        "response_type": ["code"],
        "scope": ["openid", "profile"],
        "nonce": session["oidc_nonce"],
        "redirect_uri": current_app.config["OIDC"]["redirect_uris"][0],
        "state": session["oidc_state"],
    }


def get_oidc_driver() -> Client:
    if "oidc_driver" not in g:
        g.oidc_driver = Client(client_authn_method=CLIENT_AUTHN_METHOD)
        g.oidc_driver.provider_config(current_app.config["OIDC"]["issuer"])
        from oic.oic.message import RegistrationResponse

        info = {
            "client_id": current_app.config["OIDC"]["client_id"],
            "client_secret": current_app.config["OIDC"]["client_secret"],
        }
        client_reg = RegistrationResponse(**info)
        g.oidc_driver.store_registration_info(client_reg)
    return g.oidc_driver


def login_page():
    auth_req = get_oidc_driver().construct_AuthorizationRequest(
        request_args=oidc_args(rndstr(), rndstr())
    )
    login_url = auth_req.request(
        get_oidc_driver().authorization_endpoint
    )
    print(login_url)
    return Redirect(login_url)


def get_user_id_token(query_string):
    from oic.oic.message import AuthorizationResponse

    aresp = get_oidc_driver().parse_response(
        AuthorizationResponse, info=query_string, sformat="urlencoded"
    )
    assert aresp["state"] == session["oidc_state"]
    get_oidc_driver().do_access_token_request(
        state=session["oidc_state"],
        request_args=oidc_args(session["oidc_state"]),
    )
    return get_oidc_driver().do_user_info_request(state=aresp["state"])


def init_app(app):
    app.teardown_appcontext(close_oidc_driver)


def close_oidc_driver(e=None):
    oidc_driver = g.pop("oidc_driver", None)

    if oidc_driver is not None:
        pass
