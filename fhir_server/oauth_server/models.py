from datetime import datetime, timedelta

from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_oauthlib.provider import OAuth2Provider
from flask_oauthlib.contrib.oauth2 import bind_sqlalchemy, bind_cache_grant

from fhir_server.configs.database import db
import sqlalchemy as sa


class Fhiruser(db.Model):
    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(40), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    #
    # def set_password(self, password):
    #     self.pwdhash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.pwdhash, password)

    # Required for administrative interface
    def __unicode__(self):
        return self.username


class Client(db.Model):
    """A client is the app which want to use the resource of a user.

    It is suggested that the client is registered by a user on your site,
    but it is not required.
    """
    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required
    user_id = sa.Column(sa.ForeignKey('fhiruser.id'))
    user = db.relationship('Fhiruser')

    client_id = sa.Column(sa.String(40), primary_key=True)
    client_secret = sa.Column(sa.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential ( client_type )
    is_confidential = db.Column(db.Boolean, default=False)

    _redirect_uris = sa.Column(sa.Text)
    _default_scopes = sa.Column(sa.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self._default_scopes:
            return self._default_scopes.split()
        return []

    @property
    def allowed_grant_types(self):
        return ['authorization_code', 'password', 'client_credentials',
                'refresh_token']


class Grant(db.Model):
    """A grant token is created in the authorization flow.

    It is destroyed when the authorization finished.
    In this case, it would be better to store the data in a cache,
    which would benefit a better performance.
    """
    id = sa.Column(sa.Integer, primary_key=True)

    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('fhiruser.id', ondelete='CASCADE')
    )
    user = db.relationship('Fhiruser')

    client_id = sa.Column(
        sa.String(40), sa.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = sa.Column(sa.String(255), index=True, nullable=False)

    redirect_uri = sa.Column(sa.String(255))
    expires = sa.Column(sa.DateTime)

    _scopes = sa.Column(sa.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    """A bearer: the final token that could be used by the client."""
    id = sa.Column(sa.Integer, primary_key=True)
    client_id = sa.Column(
        sa.String(40), sa.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('fhiruser.id')
    )
    user = db.relationship('Fhiruser')

    # currently only bearer is supported
    token_type = sa.Column(sa.String(40))

    access_token = sa.Column(sa.String(255), unique=True)
    refresh_token = sa.Column(sa.String(255), unique=True)
    expires = sa.Column(sa.DateTime)
    _scopes = sa.Column(sa.Text)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self


def current_user():
    if 'id' in session:
        uid = session['id']
        return Fhiruser.query.get(uid)
    return None


def cache_provider(app):
    oauth = OAuth2Provider(app)

    bind_sqlalchemy(oauth, db.session, user=Fhiruser,
                    token=Token, client=Client)

    app.config.update({'OAUTH2_CACHE_TYPE': 'simple'})
    bind_cache_grant(app, oauth, current_user)
    return oauth


def sqlalchemy_provider(app):
    oauth = OAuth2Provider(app)

    bind_sqlalchemy(oauth, db.session, user=Fhiruser, token=Token,
                    client=Client, grant=Grant, current_user=current_user)

    return oauth
