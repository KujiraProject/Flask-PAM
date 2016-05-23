# -*- coding: utf-8 -*-

from token import Token
from jose import jwt
from os import urandom

class JWT(Token):
    """JSON Web Token"""

    def __init__(self, *args, **kwargs):
        super(JWT, self).__init__(*args, **kwargs)

        self.algorithm = 'HS256'

    def generate(self):
        data = self.context.copy()
        data['username'] = self.username
        data['exp'] = int(self.expire.strftime('%s'))

        return jwt.encode(data,
                          self.secret_key,
                          algorithm=self.algorithm)

    def validate(self, token, **validation_context):
        context = jwt.decode(token,
                             self.secret_key,
                             algorithms=[self.algorithm])

        if ('ip' in validation_context and
            not context['ip'] == validation_context['ip']):
            return False

        return True
        
