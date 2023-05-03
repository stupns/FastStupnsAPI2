___
**Notification: if u use alembic, u can comment line :**
```python
# models.Base.metadata.create_all(bind=engine)
```
***

# Install alembic
```commandline
pip install alembic
alembic --help
```
And now when we deleted tables in DB with options "drop CASCADE", write next commands:

```commandline
alembic init alembic
```

## Edit Alembic configuration:

In created folders open .env file and add nest lines:

```python
from app.models import Base
from app.config import settings

config.set_main_option("sqlalchemy.url", f'postgresql+psycopg2://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')

target_metadata = Base.metadata

```

and alembic.ini change path to DB:
```text
sqlalchemy.url =
```


