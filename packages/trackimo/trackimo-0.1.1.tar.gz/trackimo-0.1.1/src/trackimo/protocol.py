# -*- coding: utf-8 -*-
"""
Protocol handler for Trackimo
"""

import logging
import sys
import requests
import os
from datetime import datetime, timedelta
from trackimo.errors import MissingInformation, UnableToAuthenticate, NoSession, CanNotRefresh, TrackimoAPI

_logger = logging.getLogger(__name__)

TRACKIMO_VERSION = 3
TRACKIMO_HOST = 'app.trackimo.com'
TRACKIMO_PORT = 443
TRACKIMO_PROTOCOL = 'https'

TRACKIMO_API_URL = f'{TRACKIMO_PROTOCOL}://{TRACKIMO_HOST}:{TRACKIMO_PORT}/api/v{TRACKIMO_VERSION}'
TRACKIMO_API_LOGIN_URL = f'{TRACKIMO_PROTOCOL}://{TRACKIMO_HOST}:{TRACKIMO_PORT}/api/internal/v2/user/login'

TRACKIMO_CLIENTID = None
TRACKIMO_CLIENTSECRET = None
SESSION = None
TRACKIMO_API_TOKEN = None
TRACKIMO_API_EXPIRES = None
TRACKIMO_REFRESH_TOKEN = None
TRACKIMO_USERNAME = None
TRACKIMO_PASSWORD = None
TRACKIMO_ACCOUNTID = None
USER = {}

def login(username=None, password=None, clientid=None, clientsecret=None):
    global SESSION
    global TRACKIMO_CLIENTID
    global TRACKIMO_CLIENTSECRET
    global TRACKIMO_API_TOKEN
    global TRACKIMO_REFRESH_TOKEN
    global TRACKIMO_API_EXPIRES
    global TRACKIMO_USERNAME
    global TRACKIMO_PASSWORD

    if clientid:
        TRACKIMO_CLIENTID = clientid
    if clientsecret:
        TRACKIMO_CLIENTSECRET = clientsecret
    if username:
        TRACKIMO_USERNAME = username
    if password:
        TRACKIMO_PASSWORD = password

    if not (TRACKIMO_USERNAME and TRACKIMO_PASSWORD):
        raise UnableToAuthenticate('Must have a username and password available')

    SESSION = requests.Session()

    scopes = [
        'locations',
        'notifications',
        'devices',
        'accounts',
        'settings',
        'geozones'
    ]

    login_payload = {
        "username": TRACKIMO_USERNAME,
        "password": TRACKIMO_PASSWORD,
        "remember_me": True,
        "whitelabel": "TRACKIMO"
    }

    auth_payload = {
        "client_id": TRACKIMO_CLIENTID,
        "redirect_uri": 'https://app.trackimo.com/api/internal/v1/oauth_redirect',
        "response_type": 'code',
        "scope": ','.join(scopes)
    }

    token_payload = {
        "client_id": TRACKIMO_CLIENTID,
        "client_secret": TRACKIMO_CLIENTSECRET,
        "code": None
    }

    response = SESSION.post(TRACKIMO_API_LOGIN_URL, json=login_payload, allow_redirects=True)
    if not response.status_code == 200:
        raise UnableToAuthenticate('Could not authenticate with login endpoint', response.status_code)

    try:
        data = api_get('oauth2/auth', auth_payload)
    except TrackimoAPI as apierror:
        _logger.debug(apierror)
        raise UnableToAuthenticate('Could not proceed with authentication after login', apierror.status_code)
    except:
        _logger.error(sys.exc_info()[0])
        exit(1)

    if not data or not 'code' in data:
        raise UnableToAuthenticate('Could not retrieve authentication code from API')

    token_payload['code'] = data['code']
    try:
        data = api_post('oauth2/token', token_payload)
    except TrackimoAPI as apierror:
        _logger.debug(apierror)
        raise UnableToAuthenticate('Could not swap a code for a token', apierror.status_code)
    except:
        _logger.error(sys.exc_info()[0])
        exit(1)

    if not data or not 'access_token' in data:
        raise UnableToAuthenticate('Could not retrieve access token code from API')

    TRACKIMO_API_TOKEN = data['access_token']
    if 'refresh_token' in data:
        TRACKIMO_REFRESH_TOKEN = data['refresh_token']

    if 'expires_in' in data:
        TRACKIMO_API_EXPIRES = datetime.now() + timedelta(seconds=int(data['expires_in'])/1000)

    _post_login()

    return {
        "token": TRACKIMO_API_TOKEN,
        "refresh": TRACKIMO_REFRESH_TOKEN,
        "expires": TRACKIMO_API_EXPIRES
    }

def _token_refresh():
    global SESSION
    global TRACKIMO_API_TOKEN
    global TRACKIMO_REFRESH_TOKEN
    global TRACKIMO_API_EXPIRES

    if not TRACKIMO_REFRESH_TOKEN:
        _logger.debug('No refresh token available. Logging in.')
        return login()

    refresh_payload = {
        "client_id": TRACKIMO_CLIENTID,
        "client_secret": TRACKIMO_CLIENTSECRET,
        "refresh_token": TRACKIMO_REFRESH_TOKEN
    }

    SESSION = requests.Session()
    TRACKIMO_API_TOKEN = None
    TRACKIMO_REFRESH_TOKEN = None
    TRACKIMO_API_EXPIRES = None

    try:
        data = api_post('oauth2/token/refresh', refresh_payload)
    except TrackimoAPI as apierror:
        _logger.debug(apierror)
        _logger.debug('Could not refresh. Trying to log in.')
        return login()
    except:
        _logger.error(sys.exc_info()[0])
        exit(1)

    if not data or not 'access_token' in data:
        _logger.debug('Could not refresh. Trying to log in.')
        return login()

    TRACKIMO_API_TOKEN = data['access_token']
    if 'refresh_token' in data:
        TRACKIMO_REFRESH_TOKEN = data['refresh_token']

    if 'expires_in' in data:
        TRACKIMO_API_EXPIRES = datetime.now() + timedelta(seconds=int(data['expires_in'])/1000)

    _post_login()

    return {
        "token": TRACKIMO_API_TOKEN,
        "refresh": TRACKIMO_REFRESH_TOKEN,
        "expires": TRACKIMO_API_EXPIRES
    }

def _post_login():
    global USER
    global TRACKIMO_ACCOUNTID

    try:
        data = api_get('user')
    except TrackimoAPI as apierror:
        _logger.debug(apierror)
        raise UnableToAuthenticate('Could not fetch user information.')
    except:
        _logger.error(sys.exc_info()[0])
        exit(1)

    if 'email' in data:
        USER['email'] = data['email']
    if 'firstName' in data:
        USER['givenName'] = data['firstName']
    if 'lastName' in data:
        USER['familyName'] = data['lastName']
    if 'user_id' in data:
        USER['id'] = data['user_id']
    if 'user_name' in data:
        USER['username'] = data['user_name']
    if 'account_id' in data:
        USER['account_id'] = data['account_id']
        TRACKIMO_ACCOUNTID = data['account_id']

def api(method='GET', path='', data=None, headers = {}):
    global SESSION
    if not SESSION:
        raise NoSession('There is no current API session. Please login() first.')

    if TRACKIMO_API_EXPIRES and datetime.now() > TRACKIMO_API_EXPIRES:
        _logger.debug('Refreshing token, it has expired.')
        _token_refresh()

    url = f'{TRACKIMO_API_URL}/{path}'

    method = method.upper()
    json = None
    params = None

    if method == 'GET':
        if data: params=data
    elif method == 'POST':
        if data: json=data
    elif method == 'DELETE':
        if data: json=data
    elif method == 'PUT':
        if data: json=data

    if TRACKIMO_API_TOKEN:
        headers['Authorization'] = f'Bearer {TRACKIMO_API_TOKEN}'

    _logger.debug({
        "url": url,
        "params": params,
        "data": json
    })

    response = SESSION.request(method, url=url, params=params, json=json, headers=headers)
    success = 200 <= response.status_code <= 299
    data = response.json()
    if not success:
        body = response.body if hasattr(response, 'body') else None
        raise TrackimoAPI('Trackimo API Call failed.', response.status_code, body, data)

    if not data: data = {}
    return data


def api_get(path=None, data=None):
    """Make a request to the Trackimo API

    Attributes:
        path (str): The path of the API endpoint
        data (object): Data to be passed as a querystring
    """
    return api('GET', path=path, data=data)

def api_post(path=None, data=None):
    return api('POST', path=path, data=data)

def api_delete(path=None, data=None):
    return api('DELETE', path=path, data=data)

def api_put(path=None, data=None):
    return api('PUT', path=path, data=data)
