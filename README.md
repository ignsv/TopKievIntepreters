# Introduction
[TopKievInterpreters](http://topkievinterpreters.com/) is used for booking interpreters for certain period, selecting special services and leaving feedback. Service involves registration, login, password recovering etc. This system has functional admin panel.

This project includes using:
* Python( 2.7.10 version)
* Flask
* SQLAlchemy
* Flask Security
* Flask Admin
* Flask Mail

# Local deployment
To run this install requirements on your virtual environment
```
pip install -r requirements.txt
```
Then just execute
```
python run.py
```
Check http://localhost:5000/ as common user or as admin(login *admin*, password *admin*). If you login as admin get http://localhost:5000/admin to test admin panel.

