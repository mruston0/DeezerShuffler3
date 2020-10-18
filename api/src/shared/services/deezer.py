from os import access
import requests
import logging
import os

logger = logging.getLogger(__name__)

class Deezer:

    def __init__(self):
        self.APP_ID = os.environ['DEEZER_APP_ID']
        self.APP_SECRET = os.environ['DEEZER_APP_SECRET']
        self.DEEZER_ACCESS_TOKEN_URL = f"https://connect.deezer.com/oauth/access_token.php?app_id={self.APP_ID}&secret={self.APP_SECRET}&code="
    
    def get_access_token_and_expiration(self, code):
        # todo: needs error handing and input validation
        url = self.DEEZER_ACCESS_TOKEN_URL + code
        response = requests.get(url)
        logger.debug(response.content)
        content_split = str(response.content).split('=')
        access_token = content_split[1].split('&')[0]
        expires = content_split[2][:-1]
        return {
            "accessToken": access_token,
            "expires": expires
        }

    def get_user(self, access_token):
        url = f"https://api.deezer.com/user/me?access_token={access_token}"
        response_json = requests.get(url).json()
        print(response_json)
        deezer_id = response_json["id"]
        deezer_name = response_json["name"]
        deezer_picture = response_json["picture_medium"]

        return {
            "id": str(deezer_id),
            "name": deezer_name,
            "picture_url": deezer_picture
        }

    def get_favourite_albums(self, access_token):
        return self._get_favourite_albums(access_token, albums=[], next=None)   

    def _get_favourite_albums(self, access_token, albums, next):
        if next:
            print(f"next url is {next}")
            url = next
        else:
            url = f"https://api.deezer.com/user/me/albums?access_token={access_token}"
        result = requests.get(url).json()

        for album in result.get('data'):
            #print(f"[DeezerAPI] Obtained {album['title']}")
            albums.append(album)
        
        if 'next' in result:
            print("Paginating....")
            return self._get_favourite_albums(access_token, albums, next=result['next'])
        print("Not paginating...")
        return albums



