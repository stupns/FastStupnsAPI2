# Backend clone  of social media app by using FastAPI
> **_NOTE:_** Previous stage development project: 
> 
> https://github.com/stupns/FastStupnsAPI
> 
___

Web-site:
https://stupns.fun/

# This API  has 4 routes:

## 1) Post route

#### This route is responsible for creating post, deleting post, updating post and Checking post

## 2) Users route

#### This route is about creating users and searching user by id

## 3) Auth route

#### This route is about login system

## 4) Vote route

#### This route is about likes or vote system and this route contain code for upvote or back vote there is not logic about down vote

# How to run locally
First clone this repo by using following command
````

git clone https://github.com/stupns/FastStupnsAPI2.git

````
then 
````

cd FastStupnsAPI2

````

Then install fastapp using all flag like 

````

pip install fastapi[all]

````

Then go this repo folder in your local computer run following command
````

uvicorn main:app --reload

````

Then you can use following link to use the  API

````

http://127.0.0.1:8000/docs 

````

## After run this API you need a database in postgres 
Create a database in postgres then create a file name .env and write the following things in you file 

````
DB_HOST = localhost
DB_PORT = 5432
DB_PASSWORD = passward_that_you_set
DB_NAME = name_of_database
DB_USERNAME = User_name
SECRET_KEY = 09d25e094faa2556c818166b7a99f6f0f4c3b88e8d3e7 
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60(base)
DB_TEST_NAME = 'name_of_database'_test

````
### Note: SECRET_KEY in this example is just a psudo key. You need to get a key for yourself and you can get the SECRET_KEY  from fastapi documentation
 
___

# Development process:

Start building:
___

[1_CONFIGURE_ALEMBIC_README.md](md/1_CONFIGURE_ALEMBIC_README.md)

[1_1_ALEMBIC_UPGRADE_README.md](md/1_1_ALEMBIC_UPGRADE_README.md)

[2_CORS_README.md](md/2_CORS_README.md)

[3_HEROKU_README.md](md/3_HEROKU_README.md)

[DIGITAL_OCEANS_README.md](md/DIGITAL_OCEANS_README.md)

[NGINX_README.md](md/NGINX_README.md)

[Firewall_README.md](md/Firewall_README.md)

[SSL_README.md](md/SSL_README.md)

[DOCKER_README.md](md/DOCKER_README.md)

[TESTS_USERS_README.md](md/TESTS_USERS_README.md)

[TESTS_POSTS_README.md](md/TESTS_POSTS_README.md)

[TESTS_VOTES_README.md](md/TESTS_VOTES_README.md)

