# learn more about event functions here: https://arc.codes/primitives/events
import json
import arc.tables
from vendor.shared.services.deezer import Deezer
from vendor.shared.repositories.deezer_shuffler import DeezerShufflerRepository


def handler(event, context):
  print(event)
  for r in event.get('Records'):
    process_record(r)
 
  return True

def process_record(record):
  msg_str = record.get('Sns', {}).get('Message')
  msg = json.loads(msg_str)
  if 'user_id' in msg:
    user_id = msg.get('user_id')
    user = DeezerShufflerRepository().get_user(user_id)
    print(f"load-albums event found user {user}")

    try:
      albums = Deezer().get_favourite_albums(user['access_token'])
      print(f"[Load Albums] found {len(albums)} albums")
      DeezerShufflerRepository().save_albums(user_id, albums)
    except Exception as e:
      print("Flagrant System Error during load-albums event handler")
      print(e)

  else:
    print("error: user_id not found in message")
