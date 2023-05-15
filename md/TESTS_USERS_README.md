# PYTEST
____

# Tests USERS

```commandline
pytest tests\test_users.py -v -s
```
____
```python
client = TestClient(app)


def test_root():
    res = client.get("/")
    assert isinstance(res.text, str)
    assert res.status_code == 200
```

```commandline
pytests --disable-warnings
pytest -v -s

pytest --disable-warnings -v -x  The pause of the test-taking process after the first failure
```

## TEST CREATE USER

```python
def test_create_user():
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201
```

## Create db

```python
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:" \
                          f"{settings.DB_PORT}/{settings.DB_NAME}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
```

__Warning:__ Fix bugs with duplicate objects in db after creating.

```python
#remove Base.metadata.create_all(bind=engine)
#remove Base = declarative_base()
@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
```

### * Example with alembic

```python
from alembic import command

def client():
    command.upgrade("head")
    yield TestClient(app)
    command.downgrade("base")
```

## Refactoring DATABASE

In database:
```python
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:" \
                          f"{settings.DB_PORT}/{settings.DB_NAME}_test"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

```

## TEST CREATE USER

```python
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

@pytest.fixture(scope="module")
def session():
    ...

@pytest.fixture(scope="module")
def client(session):
    ...
```

## TEST LOGIN USER

```python
@pytest.fixture
def session():
    ...

@pytest.fixture
def client(session):
    ...


@pytest.fixture
def test_user(client):
    user_data = {"email": "stupns@i.ua",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']}
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

```

## Export to Conftests where we should save fixtures

```python
import pytest
from .database import client, session

@pytest.fixture
def test_user(client):
    user_data = {"email": "stupns@i.ua",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user
```

## TEST INCORRECT LOGIN

```python
def test_incorrect_login(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": "WrongPassword"}
    )
    assert res.status_code == 403
    assert res.json().get('detail') == "invalid Credentials"
```

More update test:
```python
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('stupns@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('stupns@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password}
    )
    assert res.status_code == status_code
```
_________
[<-- prev step](DOCKER_README.md)_______________________________________[next step -->](TESTS_POSTS_README.md)