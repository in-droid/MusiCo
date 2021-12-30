# MusiCo


All paths accept and return only json


**USER**</br>
-- user/login/ -> accepts username, password; returns { data: { message:, username:,}, token:,} </br>
-- user/register/ -> accepts username, password, password2; returns {message:, username:, token:} </br>

**EVENT**</br>
-- event/(location) -> returns json of all events in that city </br>
-- event/(id) --> returns json for that event </br>

**ARTIST**</br>
-- artist/ -> returns json list of all artists in database
-- artist/(id) -> returns details about that artist
  
 
