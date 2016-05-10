# -*- coding: utf-8 -*-

import simplepam
import grp
import functools
from datetime import datetime, timedelta
from flask import request, abort
from os import urandom

class Auth(object):

    """Plugin for Flask which implements PAM authentication with tokens."""

    def __init__(self,
                 token_storage_type, token_type,
                 token_lifetime, refresh_token_lifetime,
                 app, development = False):
        """Initialization of Auth object
        
        :param token_storage_type: type which derives from
        token_storage.TokenStorage

        :param token_type: type which derives from token.Token

        :param token_lifetime: time interval in which token will be valid (in seconds)

        :param refresh_token_lifetime: time interval in which refresh token will be valid (in seconds)

        :param app: Flask class' instance

        :param development: flag - turning it on will always result in correct authentication
                            in decorators: auth_required and group_required
        """
        self.token_type = token_type
        self.token_storage = token_storage_type()
        self.refresh_token_storage = token_storage_type()
        self.token_lifetime = token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime
        self.init_app(app)
        self.development = development

    def init_app(self, app):
        """Saves Flask class' instance in self.app

        :param app: Flask class' instance
        """
        self.app = app

    def authenticate(self, username, password, **token_context):
        """Performs authentication using simplepam
        
        This function calls simplepam's authenticate function and returns
        status of authentication using PAM and token object (of type
        self.token_type)

        :param username: username in Linux

        :param password: password for username

        :param **token_context: additional args with keys for token generator
        """
        if simplepam.authenticate(username, password):
            expire = datetime.now() + timedelta(seconds=self.token_lifetime)
            refresh_expire = -1
            if self.refresh_token_lifetime != -1:
                refresh_expire = datetime.now() + timedelta(seconds=self.refresh_token_lifetime)

            token = self.token_type(self.app.secret_key, username, expire, **token_context)

            refresh_context = token_context.copy()
            refresh_context['refresh'] = 0
            refresh_context['refresh_salt'] = urandom(120).encode('base-64')
            refresh_token = self.token_type(self.app.secret_key, username, refresh_expire, **refresh_context)

            self.token_storage.set(token)
            self.refresh_token_storage.set(refresh_token)
            return (True, token, refresh_token)

        return (False, None, None)

    def refresh(self, token):
        """Refresh token"""

        refresh = self.refresh_token_storage.get(token)
        if refresh:
            expire = datetime.now() + timedelta(seconds=self.token_lifetime)
            refresh.context['refresh'] += 1
            refresh.context['refresh_salt'] = urandom(120).encode('base-64')
            new_token = self.token_type(self.app.secret_key, refresh.username, expire, **refresh.context)
            self.token_storage.set(new_token)

            return (True, new_token)
            

        return (False, None)

    def authenticated(self, user_token):
        """Checks if user is authenticated
        
        Checks if user is authenticated using token passed in argument
        user_token.

        :param user_token: string representing token
        """
        token = self.token_storage.get(user_token)
        if token and token.validate(user_token):
            return True

        return False

    def group_authenticated(self, user_token, group):
        """Checks if user represented by token is in group.

        :param user_token: string representing token

        :param group: group's name
        """
        if self.authenticated(user_token):
            token = self.token_storage.get(user_token)
            groups = self.get_groups(token.username)
            if group in groups:
                return True

        return False

    def get_groups(self, username):
        """Returns list of groups in which user is.

        :param username: name of Linux user
        """
        groups = []
        for group in grp.getgrall():
            if username in group.gr_mem:
                groups.append(group.gr_name)

        return groups

    # decorators
    def auth_required(self, view):
        """Decorator which checks if user is authenticated
        
        Decorator for Flask's view which blocks not authenticated requests

        :param view: Flask's view function
        """
        @functools.wraps(view)
        def decorated(*args, **kwargs):
            if request.method == 'POST':
                token = request.form['token']
                if self.development or self.authenticated(token):
                    return view(*args, **kwargs)

            return abort(403)

        return decorated

    def group_required(self, group):
        """Decorator which checks if user is in group

        Decorator for Flask's view which blocks requests from not
        authenticated users or if user is not member of specified group

        :param group: group's name
        """
        def decorator(view):
            @functools.wraps(view)
            def decorated(*args, **kwargs):
                if request.method == 'POST':
                    token = request.form['token']
                    if self.development or self.group_authenticated(token, group):
                        return view(*args, **kwargs)

                return abort(403)

            return decorated
        return decorator
