# Blockchain build with Python 

## Start Blockchain

1. Run in Container

Simply run `docker-compose up` to start up the server on port 5000 (localhost). 

2. Run locally

Make sure the latest python version (`python -v`) 3.9 is installed. 
Run `pip3 install -r requirements.txt` to install project dependencies.
Run `python server.py` to start the server (port can be specified with `-p [PORT]`, defaults to 5000).

Head over to [http://localhost:5000](http://localhost:5000) to view the UI or use postman for directly communcating with the server (import the postman collection `postman_collection.json` to help you get started more easily). 