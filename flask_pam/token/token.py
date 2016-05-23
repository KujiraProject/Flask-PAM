# -*- coding: utf-8 -*-


class Token(object):

    """Base class for all token's implementations."""

    def __init__(self, secret_key, username, expire, **context):
        """Initialize function

        :param secret_key: secret key used to sign/encrypt token

        :param username: user for whom token is generated

        :param expire: time in seconds

        :param context: additional data used to generate token
        """
        self.secret_key = secret_key
        self.username = username
        self.expire = expire
        self.context = context

        self.validate_context()

    def validate_context(self):
        return True

    def generate(self):
        """Generate token"""
        raise NotImplementedError("Token::generate must be implemented!")

    def validate(self, token, **validation_context):
        """Check if provided token is valid """
        return token == self.generate()
