# -*- coding: utf-8 -*-

class Token(object):
    
    def __init__(self, request, username, expire):
        self.request = request
        self.username = username
        self.expire = expire
        self.salt = None

    def generate(self):
        raise NotImplementedError("Token::generate must be implemented!")

    def validate(self, token):
        raise NotImplementedError("Token::validate must be implemented!")
