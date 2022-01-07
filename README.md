# MusiCo


All paths accept and return only json


**USER**</br>
-- user/login/ -> accepts username, password; returns { data: { message:, username:,}, token:,} </br>
-- user/register/ -> accepts username, password, password2; returns {message:, username:, token:} </br>
-- user/profile/ -> returns user top 10 artists and genres </br>

  **Spotify**</br>
  -- user/spotify-is-auth/ -> accepts GET request with the auth.token and returns status: True is Spotify is authenticated</br>
  -- user/spotify-auth/ -> accepts GET request with the auth.token and redirects to spotify authentication page </br>
  -- user/spotify-callback/ -> callback url used only by the backend </br>

**EVENT**</br>
-- event/?city=Ljubljana&country=Slovenia -> returns json of all events in that city </br>
-- event/(id) --> returns json for that event </br>
-- event/recommend/?city=Ljubljana&country=Slovenia -> returns recommended events (in dev)

**ARTIST**</br>
-- artist/ -> returns json list of all artists in database</br>
-- artist/(id) -> returns details about that artist</br>
  
 
