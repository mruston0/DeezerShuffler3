@app
init

@http
get /
get /authcallback
get /isloggedin
get /randomalbum

@tables
# single table design
deezer-shuffler
  id *String
  sortKey **String
  encrypt true

@events
load-albums

@static


@aws
runtime python3.8
profile mruston-personal
region ca-central-1
  