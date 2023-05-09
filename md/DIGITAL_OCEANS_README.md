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
```