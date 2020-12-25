# learn more about HTTP functions here: https://arc.codes/primitives/http
import pprint
import requests
import arc.tables
import arc.events
import jwt
import json
from vendor.shared.services.deezer import Deezer
import os

jwt_secret = os.environ['JWT_SECRET']

def handler(req, context):
  code = req.get('queryStringParameters', {}).get('code')
  state = req.get('queryStringParameters', {}).get('state')
  if not state:
    state = '/'
  
  jwt_token = None
  if code:
    dz = Deezer()
    ae = dz.get_access_token_and_expiration(code)
    user = dz.get_user(ae["accessToken"])
    # Take the user information and the access token and store it in dynamo!
    users = arc.tables.table(tablename='deezer-shuffler')
    users.put_item(
      Item={
        'id': user["id"],
        'sortKey': 'USER',
        'name': user["name"],
        'picture_url': user["picture_url"],
        'access_token': ae["accessToken"],
        'access_token_expiration': ae["expires"]
      }
    )

    arc.events.publish('load-albums', payload={"user_id": user["id"]})

    jwt_token = jwt.encode(
      {'id': user["id"]},
      jwt_secret,
      algorithm='HS256'
    )
  
  return { 
    'statusCode': 302,
    'headers': {
      'location': f'https://{state}?token={jwt_token.decode("utf-8")}'
    }
  }
    