# Flask-PAM

*Flask-PAM* is a plugin for Flask microframework which enables authentication
using Linux's PAM (**Pluggable Authentication Module**). You can check if user:

- is authenticated
- is in specified group

using views' decorators.

## Installation

To install *Flask-PAM* you should use `setup.py` script:

    python setup.py install

If you use Python's virtual environments don't forget to activate it using this
command:

    source bin/activate

in virtualenv's directory.

## Usage

Firstly, you have initialize `flask_pam.Auth` object and choose storage type for
tokens and type of token:

    from flask import Flask
     
    from flask_pam import Auth
    from flask_pam.token import Simple
    from flask_pam.token_storage import DictStorage

    app = Flask(__name__)
    auth = Auth(DictStorage, Simple, app)

When you write a view which requires authentication, you have to use
`auth_required` decorator:

    @app.route('/protected')
    @auth.auth_requied
    def protected_view():
        ....

When you want to require user to be a member of some group, you use
`group_required` decorator.

    @app.route('/group_protected')
    @auth.group_protected('wheel')
    def group_protected_view():
        ....

***Important!*** User who runs Flask application need to have access to
`/etc/shadow` file. In some cases it's only needed to add that user to `shadow`
group. Sometimes you have to create that group and change group of `/etc/shadow`
file and then add user to that group.

## Example 

You can check example which is located in `example` directory.
