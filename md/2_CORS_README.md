# CORS in FastAPI:
___
In main.py

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