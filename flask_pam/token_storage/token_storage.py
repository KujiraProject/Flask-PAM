# -*- coding: utf-8 -*-

class TokenStorage(object):
    def set(self, token):
        raise NotImplementedError("TokenStorage::set must be implemented!")

    def get(self, token):
        raise NotImplementedError("TokenStorage::get must be implemented!")

    def getByUser(self, username):
        raise NotImplementedError("TokenStorage::getByUser must be implemented!")
