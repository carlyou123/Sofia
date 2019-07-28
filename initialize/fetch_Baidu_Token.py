# coding=utf-8
import json

from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
API_KEY = 'kbuaZKSHsvjgpMrKp5IW5eVh'
SECRET_KEY = 'w3jlAvkTeNl3c4Mzc0RBYQeYHBhtCItX'
ASR_URL = 'http://vop.baidu.com/server_api'
SCOPE = 'audio_voice_assistant_get'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')

if __name__=='__main__':
    token= fetch_token()
    print(token)
    with open("../txt/token.txt", "w") as of:
        of.write(token)