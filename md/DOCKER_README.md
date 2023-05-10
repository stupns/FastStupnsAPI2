# Update new files
```commandline
cd app/src/
git pull

sudo systemctl restart api
```
__________________
# Install Docker

https://hub.docker.com/repository/

```dockerfile
FROM python:3.10.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "-host", "0.0.0.0", "--port", "8000"]
```

> __Note:__ "C:\Program Files\Docker\Docker\DockerCli.exe" -SwitchDaemon

```commandline
docker build -t fastapi .

docker image ls
```

___

```docker
version: "3.8"
services:
  api:
    build: .
    ports:
      - 8000:8000
    volumes:
      - ./:/usr/src/app
#    env_file:
#      - ./.env
    environment:
      - DB_HOST=localhost
      - DB_PORT=5432
      - DB_PASSWORD=postgres
      - DB_USERNAME=postgres
      - DB_NAME=db_fast_stupns_api2
      - SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=60

    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    depends_on:
      - postgres

  postgres:
    image: postgres
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=db_fast_stupns_api2
    volumes:
      - postgres-db:/var/lib/postgresql/data

volumes:
  postgres-db:
```

```commandline
docker compose up -d
docker ps -a
docker logs faststupnsapi2-api-1
```
_____________________

```commandline
docker login
docker image tag faststupnsapi2-api stupns/fastapistupns2

docker ps
```

```text
stupns/fastapistupns2   latest       2f376fbafe16   About an hour ago   1.01GB

```
```commandline
docker push stupns/fastapistupns2 
```
____
https://hub.docker.com/r/stupns/fastapistupns2/tags