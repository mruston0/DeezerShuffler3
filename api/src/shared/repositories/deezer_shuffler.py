import arc.tables
import datetime

class DeezerShufflerRepository:

    def __init__(self):
        self.table = arc.tables.table(tablename='deezer-shuffler')

    def get_user(self, user_id):
        item = self.table.get_item(Key={'id': user_id, 'sortKey': 'USER'})
        return item.get('Item')

    def get_user_album_count(self, user_id):
        item = self.table.get_item(Key={'id': user_id, 'sortKey': 'ALBUMCOUNT'})
        return item.get('Item', {}).get('count')

    def create_user(self, deezer_user, access_token, access_token_expiry):
        self.table.put_item(
            Item={
            'id': deezer_user["id"],
            'sortKey': 'USER',
            'name': deezer_user["name"],
            'picture_url': deezer_user["picture_url"],
            'access_token': access_token,
            'access_token_expiration': access_token_expiry
            }
        )

    def get_album(self, user_id, album_id):
        item = self.table.get_item(Key={'id': user_id, 'sortKey': f'ALBUM#{album_id}'})
        return item.get('Item')
    
    def save_albums(self, user_id, albums):
        print("[DeezerShufflerRepo] Starting save albums")
        self.table.put_item(
            Item={
                'id': user_id,
                'sortKey': 'ALBUMIMPORTPROCESS',
                'status': 'RUNNING',
                'started': datetime.datetime.utcnow().isoformat()
            }
        )
        
        count = 1
        with self.table.batch_writer() as batch:
            for a in albums:
                print(f"Batch putting {a['title']}")
                batch.put_item(
                    Item={
                        'id': user_id,
                        'sortKey': f'ALBUM#{count}',
                        'album_id': str(a['id']),
                        'title': a['title'],
                        'link': a['link'],
                        'cover': a['cover'],
                        'cover_small': a['cover_small'],
                        'cover_medium': a['cover_medium'],
                        'cover_big': a['cover_big'],
                        'artist': {
                            'id': str(a['artist']['id']),
                            'name': a['artist']['name']
                        }
                    }
                )
                count = count+1

        self.table.put_item(
            Item={
                'id': user_id,
                'sortKey': 'ALBUMIMPORTPROCESS',
                'status': 'COMPLETED',
                'started': datetime.datetime.utcnow().isoformat()
            }
        )
        
        self.table.put_item(
            Item={
                'id': user_id,
                'sortKey': 'ALBUMCOUNT',
                'count': count,
            }
        )
        
        print("[DeezerShufflerRepo] Completed save albums")