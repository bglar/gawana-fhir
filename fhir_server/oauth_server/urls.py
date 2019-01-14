from datetime import datetime, timedelta

from flask import render_template, redirect, jsonify, request, session, url_for
from flask_api.decorators import set_renderers
from flask_api.renderers import HTMLRenderer, BrowsableAPIRenderer
from werkzeug.security import gen_salt
from flask_oauthlib.provider import OAuth2Provider

from fhir_server.configs import db
from . import api_auth, Fhiruser, Client, Grant, Token, current_user

oauth = OAuth2Provider(api_auth)


@api_auth.route("/signup/", methods=("GET", "POST"))
@set_renderers(HTMLRenderer, BrowsableAPIRenderer)
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        secret = request.form.get("password")
        confirm_secret = request.form.get("password_confirm")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        email = request.form.get("email")
        user = Fhiruser.query.filter_by(username=username).first()

        if user:
            msg = "Username is already registered"
            return render_template("register.html", msg=msg)
        elif secret != confirm_secret:
            msg = "Passwords do not match"
            return render_template("register.html", msg=msg)
        else:
            user = Fhiruser(
                username=username,
                first_name=fname,
                last_name=lname,
                email=email,
                password=secret,
            )
            db.session.add(user)
            db.session.commit()

        session["user"] = user.username
        session["id"] = user.id
        return redirect(url_for("api_index"))

    user = current_user()
    return render_template("register.html", user=user)


@api_auth.route("/signin/", methods=("GET", "POST"))
@set_renderers(HTMLRenderer, BrowsableAPIRenderer)
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        secret = request.form.get("password")

        user = Fhiruser.query.filter_by(username=username, password=secret).first()

        if not user:
            msg = "Wrong username or password"
            return render_template("login.html", msg=msg)

        session["user"] = user.username
        session["id"] = user.id
        return redirect(url_for("api_index"))

    user = current_user()
    return render_template("login.html", user=user)


@api_auth.route("/signout/", methods=("GET", "POST"))
def signout():
    if "user" not in session:
        return redirect(url_for("api_auth.signin"))

    session.pop("user", None)
    session.pop("id", None)
    return redirect(url_for("api_auth.signin"))


@api_auth.route("/client/")
def client():
    user = current_user()
    if not user:
        return redirect(url_for("api_auth.signin"))
    item = Client(
        client_id=gen_salt(40),
        client_secret=gen_salt(50),
        _redirect_uris=" ".join(
            [
                "http://localhost:5000/authorized",
                "http://127.0.0.1:5000/authorized",
                "http://127.0.1:5000/authorized",
                "http://127.1:5000/authorized",
                "https://www.getpostman.com/oauth2/callback",
            ]
        ),
        _default_scopes="email",
        user_id=user.id,
    )

    db.session.add(item)
    db.session.commit()
    return jsonify(client_id=item.client_id, client_secret=item.client_secret)


@oauth.clientgetter
def load_client(client_id):
    """
    Tells which client is sending the requests, creating the getter
    with decorator

    :param client_id:
    :return:
    """
    return Client.query.filter_by(client_id=client_id).first()


@oauth.grantgetter
def load_grant(client_id, code):
    return Grant.query.filter_by(client_id=client_id, code=code).first()


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    # decide the expires time yourself
    expires = datetime.utcnow() + timedelta(seconds=100)
    grant = Grant(
        client_id=client_id,
        code=code["code"],
        redirect_uri=request.redirect_uri,
        _scopes=" ".join(request.scopes),
        user=current_user(),
        expires=expires,
    )
    db.session.add(grant)
    db.session.commit()
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return Token.query.filter_by(access_token=access_token).first()
    elif refresh_token:
        return Token.query.filter_by(refresh_token=refresh_token).first()


@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
    toks = Token.query.filter_by(
        client_id=request.client.client_id, user_id=request.user.id
    )
    # make sure that every client has only one token connected to a user
    for t in toks:
        db.session.delete(t)

    expires_in = token.pop("expires_in")
    expires = datetime.utcnow() + timedelta(seconds=expires_in)

    tok = Token(
        access_token=token["access_token"],
        refresh_token=token["refresh_token"],
        token_type=token["token_type"],
        _scopes=token["scope"],
        expires=expires,
        client_id=request.client.client_id,
        user_id=request.user.id,
    )
    db.session.add(tok)
    db.session.commit()
    return tok


@api_auth.route("/oauth/token/", methods=["GET", "POST"])
@oauth.token_handler
def access_token():
    return {}


@api_auth.route("/oauth/authorize/", methods=["GET", "POST"])
@set_renderers(HTMLRenderer, BrowsableAPIRenderer)
@oauth.authorize_handler
def authorize(*args, **kwargs):
    user = current_user()
    if not user:
        return redirect(url_for("api_auth.signin"))

    if request.method == "GET":
        client_id = kwargs.get("client_id")
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs["client"] = client
        kwargs["user"] = user
        return render_template("authorize.html", **kwargs)

    confirm = request.form.get("confirm", "no")
    return confirm == "yes"


@api_auth.route("/oauth/errors", methods=["GET"])
@oauth.invalid_response
def require_oauth_invalid():
    return jsonify(message=request.values["error"]), 401


@api_auth.route("/me/")
@oauth.require_oauth()
def me():
    user = request.oauth.user
    return jsonify(username=user.username)
