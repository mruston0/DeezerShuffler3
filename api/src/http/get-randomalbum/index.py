import jwt
import json
import random
import logging
from vendor.shared.repositories.deezer_shuffler import DeezerShufflerRepository
from jwt import algorithms

logger = logging.getLogger()
logger.setLevel(logging.INFO)

user_album_counts = {}

def handler(req, context):
    jwt_encoded = req.get('queryStringParameters', {}).get('token')

    token = jwt.decode(jwt_encoded, 'secret', algorithm='HS256')

    # Cache the album counts in a variable outside of the function 
    # context so Lambda will perist between function calls. Saves a few hits to Dynamo sometimes.
    user_id = token['id']
    if user_id not in user_album_counts:
        album_count = DeezerShufflerRepository().get_user_album_count(user_id)
        user_album_counts[user_id] = album_count
    else:
        album_count = user_album_counts[user_id]
    
    if album_count is None:
        logger.error("Error: User album count is none!")
        return {
            "statusCode": 500
        }
    
    album_choice = random.randrange(0, album_count)
    album = DeezerShufflerRepository().get_album(user_id, album_choice)
    log = {
        "album_choice": album_choice,
        "album": f"{album['artist']['name']} - {album['title']}"
    }
    logger.info(json.dumps(log))
    return {
        "statusCode": 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'content-type': 'application/json'
        },
        'body': json.dumps(album)
    }