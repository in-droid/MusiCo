# MusiCo


All paths accept and return only json


**USER**
-- user/login/ -> accepts username, password; returns { data: { message:, username:,}, token:,} </br>
-- user/register/ -> accepts username, password, password2; returns {message:, username:, token:}


**EVENT**
-- event/<location> -> returns json of all events in that city
-- event/<id> --> returns json for that artist
  
 
