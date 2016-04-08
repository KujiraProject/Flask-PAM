# -*- coding: utf-8 -*-
from hashlib import sha256
from token import Token

class Simple(Token):
    
    def generate(self):
        return sha256(self.username).hexdigest()

    def validate(self, token):
        return sha256(self.username).hexdigest() == token
