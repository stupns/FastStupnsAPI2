# PYTEST
____

# TESTS POSTS

```commandline
pytest tests\test_posts.py -v -s
```
____
## Add fixtures for TOKEN and AUTHORIZED_CLIENT

Create token:
```python
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})
```

Create authorized client:

```python
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
```

## CREATE TEST_GET_ALL_POSTS **old-v1

```python
def test_get_all_posts(authorized_client):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
```

But this test nothing know about posts, because they empty. Need create fixture with posts:

## Create fixtures TEST_POSTS **old-v1

```python
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }]
```
Here need update and commit all posts to db.
Below methods are working, but they look terrible:
```python
    # session.add_all([models.Post(title="first title", content="first content",
    #                              owner_id=test_user['id']),
    #                  models.Post(title="2nd title", content="2nd content",
    #                              owner_id=test_user['id']),
    #                  models.Post(title="3nd title", content="3nd content",
    #                              owner_id=test_user['id'])
    #                  ])
    # session.commit()
    # session.query(models.Post).all()

```
The best practics write next:
```python
@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
    ...
    }]
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()

    posts = session.query(models.Post).all()
    return posts
```

## UPDATE TEST_GET_ALL_POSTS **old-v2

```python
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)

    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # print(posts_list)

    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
```

result will be:
```text
[PostOut(Post=Post(title='3rd title', content='3rd content', published=True, id=4, created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 700653, tzinfo=datetime.timezone(dat
etime.timedelta(seconds=10800))), owner_id=1, owner=UserOut(id=1, email='stupns@i.ua', created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 688078, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))))), 
votes=0), PostOut(Post=Post(title='2nd title', content='2nd content', published=True, id=2, created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 700653, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))
), owner_id=1, owner=UserOut(id=1, email='stupns@i.ua', created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 688078, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))))), votes=0), PostOut(Post=Post(tit
le='3rd title', content='3rd content', published=True, id=3, created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 700653, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))), owner_id=1, owner=UserOut(id
=1, email='stupns@i.ua', created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 688078, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))))), votes=0), PostOut(Post=Post(title='first title', content='firs
t content', published=True, id=1, created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 700653, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))), owner_id=1, owner=UserOut(id=1, email='stupns@i.ua', created_at=datetime.datetime(2023, 5, 12, 12, 23, 46, 688078, tzinfo=datetime.timezone(datetime.timedelta(seconds=10800))))), votes=0)]

```

## TEST UNAUTHORIZED USER GET ALL POSTS

```python
def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
```

## TEST UNAUTHORIZED USER GET ONE POST

```python
def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
```

## TEST GET ONE POST NOT EXIST

```python
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404
```

## TEST GET ONE POST 

```python
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(Post=test_posts[0], votes=0)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
```

## TEST CREATE POST

```python
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']
```

## TEST CREATE POST DEFAULT PUBLISHED TRUE

```python
def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "aasdfjasdf"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
```

## TEST UNAUTHORIZED USER CREATE POST

```python
def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/", json={"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401
```

## TEST UNAUTHORIZED USER DELETE POST

```python
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
```

## TEST DELETE POST SUCCESS

```python
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")
    
    assert res.status_code == 204
```

## TEST DELETE POST NON EXIST

```python
def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404
```

## TEST DELETE OTHER USER POST

> __Note:__ The first step is to create another user in fixtures and update this user in publications:

```python
@pytest.fixture
def test_user2(client):
    user_data = {"email": "stupns123@i.ua",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
    ..., {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]
    
```

And now we should create test checking:

```python
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
```

## TEST UPDATE POSTS

```python
def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
```

## TEST UPDATE OTHER USER POST

```python
def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
```

## TEST UNAUTHORIZED USER UPDATE POST

```python
def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
```

## TEST UPDATE POST NON EXIST

```python
def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "update content",
        "id": test_posts[3].id

    }
    res = authorized_client.put(
        f"/posts/8000000", json=data)

    assert res.status_code == 404
```
___