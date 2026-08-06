
mkdir templates 
python3 scaffold.py country name
python3 scaffold.py identity name
python3 scaffold.py track composer_artist title
python3 scaffold.py socialmedia name
python3 scaffold.py sharemusic track_id:references track_id:references user_id:references
python3 scaffold.py user username email password country_id:references phone identity_id:references
python3 scaffold.py cli content user_id:references
