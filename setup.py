# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='Flask-PAM-Reloaded',
      version='0.1.2',
      description='Flask authentication using PAM',
      author='Kacper Kołodziej, Steven Yang',
      author_email='yangzhaofengsteven@gmail.com',
      url='https://github.com/yangzhaofeng/Flask-PAM',
      packages=['flask_pam', 'flask_pam.token', 'flask_pam.token_storage',],
      install_requires=[
        'simplepam>=0.1.5',
        'Flask>=0.10.1',
        'python-jose>=0.6.1',
      ],    
)
