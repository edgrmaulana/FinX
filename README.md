# Requirements

- Python 3.8 or above
- PostgreSQL

# Installation

- Go to specified directory which the app will be installed
- Create virtual environment for your python

`python3 -m venv venv` or `virtualenv venv`

- Clone the project from repository

`git clone [git url]`

- Go to project directory

`cd [project url]`

- Activate yout virtual environment

`source ../venv/bin/activate`

- Install the dependencies

`pip install -r requirements.txt`

# Preparation

- Check your project

`./manage.py check`

- Make migrations

`./manage.py makemigrations`

- Migrate

`./manage.py migrate`

- Check the server again

`./manage.py check`