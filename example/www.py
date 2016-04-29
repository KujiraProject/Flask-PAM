from flask import Flask, request
from flask_pam import Auth
from flask_pam.token_storage import DictStorage
from flask_pam.token import Simple
import json
import www_config

app = Flask(__name__)
app.secret_key = 'test_secret_key'
auth = Auth(DictStorage, Simple, app)

@app.route('/')
def index():
    return json.dumps({'status': True, 'data': None})

@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    if request.method == 'POST':
        if not (request.form['username'] and request.form['password']):
            return json.dumps({
                'status': False,
                'errors': [
                    'username or password is not set!'
                ]
            })

        username = request.form['username'].encode('ascii')
        password = request.form['password'].encode('ascii')

        result = auth.authenticate(username, password)

        role = None
        user_groups = auth.get_groups(username)
        for group in www_config.groups:
            if group in user_groups:
                role = group
                break

        if result[0]:
            return json.dumps({
                'status': True,
                'data': [
                    {
                        'type': 'tokens',
                        'id': result[1].generate(),
                    },
                    {
                        'type': 'roles',
                        'id': role,
                    }
                ]
            })

    return json.dumps({
        'status': False,
        'errors': [
            'authentication faild!',
        ]
    })

@app.route('/protected', methods=['POST', 'GET'])
@auth.auth_required
def protected():
    return json.dumps({
        'status': True,
        'data': None,
    })

@app.route('/group1_protected', methods=['POST', 'GET'])
@auth.group_required(www_config.groups[0])
def gprotected1():
    return json.dumps({
        'status': True,
        'data': {
            'id': 'groups',
            'type': www_config.groups[0]
        }
    })

@app.route('/group2_protected', methods=['POST', 'GET'])
@auth.group_required(www_config.groups[1])
def gprotected2():
    return json.dumps({
        'status': True,
        'data': {
            'id': 'groups',
            'type': www_config.groups[1]
        }
    })


if __name__ == '__main__':
    app.debug = True
    app.run()
