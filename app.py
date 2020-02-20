
from flask import Flask, render_template, jsonify, redirect, session, url_for, request, _request_ctx_stack
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from functools import wraps
from os import environ as env
from werkzeug.exceptions import HTTPException
from dotenv import load_dotenv, find_dotenv

import requests
import json
import http.client
import socket
import constants


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)

app = Flask(__name__, static_url_path='/public', static_folder='./public')
app.secret_key = constants.SECRET_KEY
app.debug = True

oauth = OAuth(app)



class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

auth0 = oauth.register(
    'auth0',
    client_id='mUwNtuLUgKkYCfsicjvx67bzWkfoeBLl',
    client_secret='Rug9Yj8uRTSLcOuNMcfbENWX8BO2IkV1dqjDcMpN_XYAwwcTrFXx7LgsM78a3jnc',
    api_base_url='https://dev-1w61yevw.auth0.com',
    access_token_url='https://dev-1w61yevw.auth0.com/oauth/token',
    authorize_url='https://dev-1w61yevw.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')


from flask import Flask, render_template, jsonify
#from GeekText.views.index import bp as index_bp




#app.register_blueprint(index_bp)

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/wishlist')
def wishlist():
    return render_template('/wishlist.html')

@app.route('/shoppingcart')
def shoppingcart():
    return render_template('shoppingcart.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)
    #return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('index.html',
                           userinfo=session[constants.PROFILE_KEY],
                           userinfo_pretty=json.dumps(session[constants.JWT_PAYLOAD], indent=4))

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=env.get('PORT', 3000))


