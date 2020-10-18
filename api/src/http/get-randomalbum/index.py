import jwt
import json
import random
from vendor.shared.repositories.deezer_shuffler import DeezerShufflerRepository

from jwt import algorithms

def handler(req, context):
    jwt_encoded = req.get('queryStringParameters', {}).get('token')

    token = jwt.decode(jwt_encoded, 'secret', algorithm='HS256')

    user_id = token['id']
    album_count = DeezerShufflerRepository().get_user_album_count(user_id)
    if album_count is None:
        print("Error: User album count is none!")
        return {
            "statusCode": 500
        }
    album_choice = random.randrange(0, album_count)
    album = DeezerShufflerRepository().get_album(user_id, album_choice)
    print(f"Returning album {album} for album_choice {album_choice}")

    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'content-type': 'application/json'
        },
        'body': json.dumps(album)
    }