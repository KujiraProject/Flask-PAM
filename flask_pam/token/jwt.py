# -*- coding: utf-8 -*-

from token import Token
from jose import jwt
from os import urandom

class JWT(Token):
    """JSON Web Token"""

    def __init__(self, algorithm = 'HS256', *args, **kwargs):
        super(Token, self).__init__(*args, **kwargs)

        self.algorithm = algorithm
        self.context['username'] = self.username

        if not 'salt' in self.context:
            self.context['salt'] = urandom(256)

    def generate(self):
        return jwt.encode(self.context,
                          self.secret_key,
                          algorithm=self.algorithm)

    def validate(self, token):
        context = jwt.decode(token,
                             self.secret_key,
                             algorithms=[self.algorithm])

        return context == self.context
        
