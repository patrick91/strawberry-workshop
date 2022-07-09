# Write a production ready GraphQL API using Python

Hello! This is the code companion for the "Write a production ready GraphQL API
using Python" tutorial.

## To get started

This tutorial assumes you're have python 3.10 and poetry installed. To install
poetry you can following the guide here
[https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).

If you can't install Python 3.10 or are having issues with dependencies you can
try this project on Gitpod.io:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/patrick91/strawberry-workshop)

## Setup

run the following command to get the project up and running:

```bash
poetry install
poetry run poe import-data
poetry run poe migrate
poetry run poe server
```

Once the server is running you can check if everything is fine by going to
https://localhost:8000/graphql.


## Running tests

```bash
poetry run poe test
```
