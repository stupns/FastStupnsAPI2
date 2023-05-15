# CORS in FastAPI:
___
CORS stands for Cross-Origin Resource Sharing. It's a security feature implemented in web browsers that restricts web pages from making requests to a different domain than the one that served the original web page. This is to prevent malicious scripts on a page from accessing resources on another domain, which could lead to security vulnerabilities.

To enable cross-origin resource sharing, the server hosting the requested resource needs to explicitly allow requests from other domains. This is done by including certain HTTP headers in the server response to the client's request. These headers specify which domains are allowed to access the requested resource and what type of requests are allowed.

CORS is an important security feature in web development, as it helps prevent cross-site scripting attacks and other security vulnerabilities. It's often used in RESTful API development to allow clients from different domains to access the API resources.

### In main.py

```python
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Now u can open google.com and in Console send API without error CORS:

```commandline
fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
```

result will be:
```text
Promise {<pending>}[[Prototype]]: Promise[[PromiseState]]: "fulfilled"[[PromiseResult]]: undefined

{message: 'Hello world'}
message: "Hello world"

[[Prototype]]: Objectconstructor: ƒ Object()hasOwnProperty:
  ...
...
```
___
[<-- prev step](1_1_ALEMBIC_UPGRADE_README.md)_______________________________________[next step -->](3_HEROKU_README.md)