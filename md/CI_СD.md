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
