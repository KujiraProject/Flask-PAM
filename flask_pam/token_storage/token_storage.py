# -*- coding: utf-8 -*-

class TokenStorage(object):

    """Base class for all implementations for tokens' storage interfaces."""

    def set(self, token):
        """Adds token to storage
        
        :param token: object of class which derives from Token
        """
        raise NotImplementedError("TokenStorage::set must be implemented!")

    def get(self, token):
        """Loads token from storage using token string

        :param token: token string
        """
        raise NotImplementedError("TokenStorage::get must be implemented!")

    def getByUser(self, username):
        """Loads token object from utorage using his username"""
        raise NotImplementedError("TokenStorage::getByUser must be implemented!")
