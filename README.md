# ReStocked

Stock App for novice investors!

Project consumes data from listed stock API(s) below:

* https://iextrading.com/developer/
* https://www.alphavantage.co/ ( in-research )

All codes from this project are for *study* purpose only and **should not** be deployed in a PRODUCTION
or in an enterprise environment.

## Report Issues
To report an issue that can be ideas, suggestions for new features, or even a bug found during your tests, 
please follow github https://help.github.com/articles/creating-an-issue/ 

## Disclaimer
* This software is built for study purpose only.  
* I do not offer any support, you can fork or use this software with your own risk.
* This software may use third-party libraries and modules, check their licenses and legal aspects before to install in your environment.
* Any data resulted of this program execution such as stock recommendation, stock price etc should not be used as source for trading or any investments.

## How to contribute
Forks need to be authorized and PRs  submitted for code review.

## Prepare development machine to run ReStocked

1. Start-up MongoDB service or docker container and make sure it is listening on port 27017. MongoDB Compass is optional
   but strongly recommended for better DB data management https://docs.mongodb.com/compass/master/install/

2. create python virtual environment and install all modules listed in requirements.txt. For better alternative
   you can run the followed command to initialize this step: $ make init

3. Load your database executing the script src/db/update_db_using_iex_API.py
   As alternative for this step you can run: $ make db-import

4. Start-up Flask application, src/web/app.py and go to http://127.0.0.1:5000/
   As alternative for this step you can run:


## Running MongoDB in Docker container

Install and start docker service in your machine
Linux/Fedora: sudo systemctl docker start
MacOS: https://docs.docker.com/docker-for-mac/install/

pull mongo container [ https://hub.docker.com/_/mongo/ ]
docker pull mongo

create/start mongo container for first time
docker run --name mongodb -p 27017:27017 -d mongo

stop mongo container
docker stop mongodb

start mongo
docker start mongodb

check container is running
docker ps
docker ps -a