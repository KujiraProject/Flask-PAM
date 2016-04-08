# -*- coding: utf-8 -*-

import simplepam
import grp
import pwd
import functools
from datetime import datetime, timedelta
from flask import request, abort

class Auth:
    
    def __init__(self, token_storage_type, token_type, app = None):
        self.token_type = token_type
        self.token_storage = token_storage_type()
        self.init_app(app)

    def init_app(self, app):
        self.app = app

    def authenticate(self, username, password):
        if simplepam.authenticate(username, password):
            expire = datetime.now() + timedelta(minutes=30)
            token = self.token_type(request, username, expire)
            self.token_storage.set(token)
            return (True, token)

        return (False, None)

    def authenticated(self, user_token):
        token = self.token_storage.get(user_token)
        if token and token.validate(user_token):
            return True

        return False

    def group_authenticated(self, user_token, group):
        if self.authenticated(user_token):
            token = self.token_storage.get(user_token)
            groups = self.get_groups(token.username)
            if group in groups:
                return True

        return False

    def get_groups(self, username):
        groups = []
        for group in grp.getgrall():
            if username in group.gr_mem:
                groups.append(group.gr_name)

        return groups

    # decorators
    def auth_required(self, view):
        @functools.wraps(view)
        def decorated(*args, **kwargs):
            if request.method == 'POST':
                token = request.form['token']
                if self.authenticated(token):
                    return view(*args, **kwargs)

            return abort(403)

        return decorated

    def group_required(self, group):
        def decorator(view):
            @functools.wraps(view)
            def decorated(*args, **kwargs):
                if request.method == 'POST':
                    token = request.form['token']
                    if self.group_authenticated(token, group):
                        return view(*args, **kwargs)

                return abort(403)

            return decorated
        return decorator
