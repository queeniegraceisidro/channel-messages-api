# Overview

This project is a messaging application with a feature of channels (rooms).
It allows users to create different channels based on topics or interests and communicate with other users within those
rooms.

# Setup

### Django

Python Version: 3.10

#### Install dependencies with Poetry

```bash
$ poetry install
```

#### Setup .env

##### Create ".env" file on root project and fill it up

There should be a sample called .env.sample to base on

#### Migrate migrations

```bash
$ poetry run python manage.py migrate
```

#### Run the development server

```bash
$ poetry run python manage.py runserver
```

#### Run tests

```bash
$ poetry run pytest
```
