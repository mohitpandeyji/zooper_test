# API

## Prerequisites

```
ubuntu 20.04
Python 3.8.2
pip 20.1
virtualenv
```

## Run Development Server

```
bash
virtualenv py_venv
source py_venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0:8000
```