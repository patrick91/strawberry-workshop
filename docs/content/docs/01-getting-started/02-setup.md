+++
title = "Setup"
draft = false
weight = 11
sort_by = "weight"
template = "docs/page.html"
slug = "setup"

[extra]
toc = true
top = false
+++

## Option 1: using gitpod

This is the easiest way to get started, you can use gitpod to run the workshop
in your browser.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/patrick91/strawberry-workshop)

Gitpod is a service that allows you to run a development environment in the
cloud. It will automatically clone the repository and install all the
dependencies.

Once you have opened the link, you will be asked to login with GitHub, once you
have done that you will be able to start the workshop.

## Option 2: using your own machine

If you prefer to use your own machine, you can clone the repository and install
the dependencies.

### Clone the repository

```bash
git clone https://github.com/patrick91/strawberry-workshop.git
cd strawberry-workshop
```

### Create the virtualenv and install the dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run the tests to make sure everything is working

```bash
pytest
```

### Import data

To import the data we will use the built-in cli:

```bash
python manage.py migrate

python cli.py import-feeds \
    https://talkpython.fm/episodes/rss \
    https://realpython.com/podcasts/rpp/feed \
    https://pythonbytes.fm/episodes/rss \
    https://www.pythonpodcast.com/feed/mp3/
```
