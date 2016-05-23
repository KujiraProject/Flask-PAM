# -*- coding: utf-8 -*-
from hashlib import sha256
from token import Token
import logging

log = logging.getLogger(__name__)

class Simple(Token):

    """Simple token implementation. Only for testing purposes."""

    def generate(self):
        log.info("Generating Simple token for user '%s'", self.username)
        return sha256(self.username + str(self.context)).hexdigest()
