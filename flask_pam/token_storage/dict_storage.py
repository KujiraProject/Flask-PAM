# -*- coding: utf-8 -*-

from token_storage import TokenStorage
from datetime import datetime

class DictStorage(TokenStorage):
    """Tokens' storage which uses Python's dictionaries"""
    def __init__(self):
        self.tokens = {}
        self.users = {}

    def get(self, token):
        if token in self.tokens:
            t = self.tokens[token]
            if t.expire >= datetime.now():
                return t

        return None

    def set(self, token):
        self.tokens[token.generate()] = token
        self.users[token.username] = token

    def getByUser(self, username):
        if username in self.users:
            t = self.users[username]
            if t.expire >= datetime.now():
                return t

        return None

