## HEROKU:

https://devcenter.heroku.com/articles/getting-started-with-python#set-up

```commandline
heroku login
```

___

```commandline
heroku create fastapi-stupns
git push heroku main
```

_____
Create file Procfile

```text
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
```

For check logs:

```commandline
heroku logs --tail
```

Fix errors:

```commandline
heroku addons:create heroku-postgresql:mini
```

Open Datastories>heroku-postgresql > Settings > Credentials
copy data and paste in 
fastapi-stupns > Settings > Config Vars
![](..\img\1.png)

```commandline
heroku ps:restart

heroku apps:info fastapi-stupns

```
work url:

https://fastapi-stupns.herokuapp.com/