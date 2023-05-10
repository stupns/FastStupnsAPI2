https://cloud.digitalocean.com/droplets/

create tagname in field hostname:
ubuntu-fastapi

Open terminal:
![](..\img\2.png)

copy ip-addrest and connect to ssh wirh previlegies root:
```commandline
ssh root@165.232.127.31

sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip

sudo pip3 install virtualenv
sudo apt install postgresql postgresql-contrib -y
```
## POSTGRES

Error with authenticates, because in default we login as root, but local machine postgres wait user as postgres,
next command show  all registers users in ubuntu/

```commandline
sudo cat /etc/passwd
```

In results we can look user postgres:
```text
...
...
postgres:x:113:122:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
```

Change user it commands :
```commandline
su - postgres
```



if u change user profile from root to postgres use next:
```commandline
psql -U postgres

# next steps need add pasword to DB

\password postgres

:pass
:re-pass

-Complete-

# exit from terminal db
\q 
```
___
Logout from user postgres:
```commandline
exit
cd /etc/postgresql/14/main

sudo vi postgresql.conf
```

add next line:
```text
# - Connection Settings -
listen_addresses = '*'
```

> __Note:__ **_Esc + :wq_**  _- exit from VI with savings_

It unlock posibbles connect to my DB from all ip-addresses

```commandline
sudo vi pg_hba.conf
```
change next variable form peer to scram-sha-256
```text
# Database administrative login by Unix domain socket
local   all             postgres                                scram-sha-256

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     scram-sha-256
# IPv4 local connections:
host    all             all             0.0.0.0/0               scram-sha-256
# IPv6 local connections:
host    all             all             ::/0                    scram-sha-256
# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            scram-sha-256
host    replication     all             ::1/128                 scram-sha-256
```

Restart postgres after changing configuration files :
```commandline
systemctl restart postgresql
```

Now u can login as root to db:

```commandline
psql -U postgres
```
<p style="color:green">--Complete--</p>

## Create server
Name: fastapi-prod

Hostname: 165.232.127.31  #my local-ip ubuntu

Password: postgres

<p style="color:green">--Complete--</p>

## Create user for ubuntu with previlegies root

```commandline
adduser stupns
usermod -aG sudo stupns


root@ubuntu-fastapi: exit
C:\Users\helbo> exit
ssh stupns@165.232.127.31
```
<p style="color:green">--Complete--</p>
Result:

```text
stupns@ubuntu-fastapi:~$
```

U can see that now for user has been created new folder:
```commandline
$pwd
/home/stupns
```
## Create folder with project

```commandline
mkdir app
cd app
virtualenv FastStupnsAPI2
source FastStupnsAPI2/bin/activate

deactivate

mkdir src
cd src
git clone https://github.com/stupns/FastStupnsAPI2.git .

cd ..
source FastStupnsAPI2/bin/activate
cd src
pip install -r requirements.txt
```
_____
__Warning:__ Fix bugs :

```text
Failed to build psycopg2
ERROR: Could not build wheels for psycopg2, which is required to install pyproject.toml-based projects
```

Fix :
```commandline
deactivate
sudo apt install libpq-dev
```
____

## Run project:

```commandline
 uvicorn app.main:app --reload
 
```
__Warning:__ Fix bugs :
```text
DB_HOST
  field required (type=value_error.missing)
DB_PORT
  field required (type=value_error.missing)
DB_PASSWORD
  field required (type=value_error.missing)
DB_USERNAME
  field required (type=value_error.missing)
DB_NAME
  field required (type=value_error.missing)
SECRET_KEY
  field required (type=value_error.missing)
ALGORITHM
  field required (type=value_error.missing)
ACCESS_TOKEN_EXPIRE_MINUTES
  field required (type=value_error.missing)
```

Next steps:
```commandline
cd ~
touch .env
vi .env
```

Add all variables from env and save.

```commandline
 set -o allexport; source /home/stupns/.env; set +o allexport
```

And when we write **_printenv_** we can see that all variables added to systemvars.
__Warning:__ But when we reboot machine all variables will be resets.

Fix next:
```commandline
 vi .profile
```
and add previous code:
```text 
set -o allexport; source /home/stupns/.env; set +o allexport
```
save and reboot:
```commandline
sudo reboot 
```
<p style="color:green">--Complete--</p>

""

## Create db and check connection

db_name: db_fast_stupns_api2

```commandline
alembic upgrade head
```
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 86d42f033b57, create posts table
INFO  [alembic.runtime.migration] Running upgrade 86d42f033b57 -> 8a33c1201619, add content column to posts table
INFO  [alembic.runtime.migration] Running upgrade 8a33c1201619 -> 73d00a5fcf7b, add user table
INFO  [alembic.runtime.migration] Running upgrade 73d00a5fcf7b -> 00e241a4645a, add foreign-key to posts table
INFO  [alembic.runtime.migration] Running upgrade 00e241a4645a -> b09e5d38b78b, add last few columns to posts table
INFO  [alembic.runtime.migration] Running upgrade b09e5d38b78b -> 7b349241c439, auto-vote
INFO  [alembic.runtime.migration] Running upgrade 7b349241c439 -> d88845fc56fe, add phone number
```
<p style="color:green">--Complete--</p>

## Start server 

```commandline
uvicorn app.main:app 
```
http://127.0.0.1:8000

__Warning:__ Fix troubles

```commandline
uvicorn --host 0.0.0.0 app.main:app 
```
http://165.232.127.31:8000/

## Install Gunicorn and run workers for fast work

```commandline
pip install gunicorn
pip install uvloop
pip install uvtools

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
```

Change code for background mode:

create file gunicorn.service:
```text
[Unit]
Description=demo fastapi application
After=network.target

[Service]
User=stupns
Group=www-data
WorkingDirectory=/home/stupns/app/src/
Environment="PATH=/home/stupns/app/FastStupnsAPI2/bin"
EnvironmentFile=/home/stupns/.env
ExecStart=/home/stupns/app/FastStupnsAPI2/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```
 
```commandline
cd etc/systemd/system/
sudo vi api.service
```
and paste code from gunicorn.service.
```commandline
systemctl start api
systemctl status api
systemctl enable api
```

<p style="color:green">--Complete--</p>