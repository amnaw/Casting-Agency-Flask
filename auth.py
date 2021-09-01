import json
from flask import request, _request_ctx_stack, abort, Flask
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-04zvrt8l.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Casting-Agency'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)
    if auth_header is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected within the request.'
        }, 401)

    # the token format is "Bearer <Token-Characters>" and token_parts length must be 2
    token_parts = auth_header.split()
    if (token_parts[0].lower() != 'bearer') or len(token_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must contains "Bearer Token".'
        }, 401)

    token = token_parts[1]
    return token


def check_permissions(permission, payload):
    # the payload is deccoded
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not found in JWT payload.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)
    return True


def verify_decode_jwt(token):
    # Get the public key from AUTH0 
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header:
    # to unpack the header of the (jwt)token to determine if we have the correct key!
    # cuz the jwt header contains the key id we are looking for
    # to pick the right key used in validation
    unverified_header = jwt.get_unverified_header(token)
    
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
    # Choose our key by Iterate over all keys received
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    # Finally, verify and decode the payload!!!
    if rsa_key:
        try:
            # Use the Token, Key to validate JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
            
        # some standard Auth0 exceptions   
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)
            except:
                abort(403)
                
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator