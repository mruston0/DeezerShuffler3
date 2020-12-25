import jwt
import json
import os

jwt_secret = os.environ['JWT_SECRET']

def handler(req, context):
    # iterate to find the user cookie
    isLoggedIn = False
    if "cookies" in req:
        for c in req.get("cookies"):
            if c.startswith('user'):
                jwt_encoded = c.split('=')[1]
                token = jwt.decode(jwt_encoded, jwt_secret, algorithm='HS256')
                if token.get("id"):
                    isLoggedIn = True
    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'content-type': 'application/json'
        },
        'body': json.dumps({"isLoggedIn": isLoggedIn}),
        'statusCode': 200,
    }