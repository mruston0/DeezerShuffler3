# copy index.html from front-end into api/public folder so it gets automatically deployed to s3
$staging_api = "https://api-staging.deezershuffler.net"
$staging_deezer_app_id = "438502"

.\copy-front-end.ps1
Push-Location -Path '..\api'
# Set Environment variables in the front end
((Get-Content -path public\index.html -Raw) -replace 'const API_ENDPOINT_URI = "http://lvh.me:3333";',"const API_ENDPOINT_URI = `"$staging_api`";") | Set-Content -Path public\index.html
((Get-Content -path public\index.html -Raw) -replace 'const DEEZER_APP_ID = "438242";',"const DEEZER_APP_ID = `"$staging_deezer_app_id`";") | Set-Content -Path public\index.html
arc deploy
Pop-Location