# -*- coding: utf-8 -*-

from token import Token
from jose import jwt
import logging

log = logging.getLogger(__name__)


class JWT(Token):
    """JSON Web Token"""

    def __init__(self, *args, **kwargs):
        super(JWT, self).__init__(*args, **kwargs)

        self.algorithm = 'HS256'
        log.info("JWT (algorithm: %s) initialized!", self.algorithm)

    def generate(self):
        data = self.context.copy()
        data['username'] = self.username
        data['exp'] = int(self.expire.strftime('%s'))

        log.info("Generating JWT for user '%s'", self.username)
        return jwt.encode(data,
                          self.secret_key,
                          algorithm=self.algorithm)

    def validate(self, token, **validation_context):
        context = jwt.decode(token,
                             self.secret_key,
                             algorithms=[self.algorithm])

        if 'ip' in validation_context and \
           not context['ip'] == validation_context['ip']:
            log.warning("Token is invalid!")
            return False

        return True
