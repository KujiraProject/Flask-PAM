from flask import Flask, request
from flask_pam import Auth
from flask_pam.token_storage import DictStorage
from flask_pam.token import Simple
import json
import www_config

app = Flask(__name__)
auth = Auth(DictStorage, Simple, app)

@app.route('/')
def index():
    return json.dumps({'status': True})

@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username'].encode('ascii')
        password = request.form['password'].encode('ascii')

        result = auth.authenticate(username, password)
        if result[0]:
            return json.dumps({
                'status': True,
                'token': result[1].generate(),
            })

    return json.dumps({
        'status': False,
    })

@app.route('/protected', methods=['POST', 'GET'])
@auth.auth_required
def protected():
    return json.dumps({'status': True})

@app.route('/group1_protected', methods=['POST', 'GET'])
@auth.group_required(www_config.groups[0])
def gprotected1():
    return json.dumps({'status': True, 'group': www_config.group1})

@app.route('/group2_protected', methods=['POST', 'GET'])
@auth.group_required(www_config.groups[1])
def gprotected2():
    return json.dumps({'status': True, 'group': www_config.group2})


if __name__ == '__main__':
    app.debug = True
    app.run()
