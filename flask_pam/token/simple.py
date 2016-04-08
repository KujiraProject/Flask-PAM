# -*- coding: utf-8 -*-
from hashlib import sha256
from token import Token

class Simple(Token):
    """Simple token implementation. It's not safe. Only for testing purposes!"""

    def generate(self):
        return sha256(self.username).hexdigest()
