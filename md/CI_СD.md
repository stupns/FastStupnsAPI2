# CI\CD in FastAPI:
___

- Continuous integration - automated process to build, package and test applications

- Continuous Delivery - Picks up where continuous integration ands and automated the delivery of applications.

Current manual process:
- Make Changes to code
- Commit changes
- Run tests
- Build image
- Deploy

![](..\img\CI-CD.png)

____
https://docs.github.com/ru/actions

```text
name: Build and Deploy Code

on: [push, pull_request]

jobs:
  jobs1:
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: Install python version 3.11
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
```
![](..\img\depl1.png)

## Add tests

```text
name: Build and Deploy Code

on: [push, pull_request]

jobs:
  jobs1:
    environment:
      name: testing
    runs-on: ubuntu-latest
    steps:
      - name: pulling git repo
        uses: actions/checkout@v2
      - name: Install python version 3.11
        uses: actions/setup-python@v2
        with:
          python-version: "3.11"
      - name: update pip
        run: python -m pip install --upgrade pip
      - name: install all dependencies
        run: pip install -r requirements.txt
      - name: test with pytest
        run: |
          pip install pytest
          pytest
```

We have error in git with env variables. Fix:

Repository>Settings>Secrets: and add all variables
![](..\img\repos_secrets.png)

```text
jobs:
  jobs1:
    
    env:
      DB_HOST: ${{secrets.DB_HOST}}
      DB_PORT: ${{secrets.DB_PORT}}
      DB_PASSWORD: ${{secrets.DB_PASSWORD}}
      DB_USERNAME: ${{secrets.DB_USERNAME}}
      DB_NAME: ${{secrets.DB_NAME}}
      SECRET_KEY: ${{secrets.SECRET_KEY}}
      ALGORITHM: ${{secrets.ALGORITHM}}
      ACCESS_TOKEN_EXPIRE_MINUTES: ${{secrets.ACCESS_TOKEN_EXPIRE_MINUTES}}
```

Next error with DB. Fix:

```text
    services:
      postgres:
        image: postgres
        env:
          POSTGRES_PASSWORD: ${{secrets.DB_PASSWORD}}
          POSTGRES_DB: ${{secrets.DB_NAME}}_name
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
```