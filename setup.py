# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='Flask-PAM',
      version='0.1',
      description='Flask authentication using PAM',
      author='Kacper Kołodziej',
      author_email='kacper@kolodziej.in',
      url='https://github.com/KujiraProject/Flask-PAM',
      packages=['flask_pam', 'flask_pam.token', 'flask_pam.token_storage',],
      install_requires=[
        'simplepam>=0.1.5',
        'Flask>=0.10.1',
        'python-jose>=0.6.1',
      ],    
)
