
## Installation

To run this application on linux in local you need python3.7.9 or 3.8.0,
pip and virtalenv or venv.

### Python, pip and virtualenv

Install python and pip (comes built in with python 3.8.0 or higher)

Create and activate a virtual environment.

### Clone project from github:

git clone https://github.com/Matje1979/zajednica.git

cd into zajednica folder (the root project folder)

### Install dependencies:

pip3 install -r requirements.txt

## Settings

Create .env file in the root of the project (zajednicastanara)

Copy in it the content of .env.example file.

### Set database:

python manage.py migrate (or python3 manage.py migrate)

Go to zajednica/users/apps.py and comment out the ready function.

This is to prevent creating new profiles for users
when records are imported.

### Import data:

python manage.py loaddata db.json

Uncomment ready function in zajednica/users/apps.py

### Set static files:

python3 manage.py collectstatic

### Run project:

python3 manage.py runserver

Check website at localhost:8000

### Create admin user

python manage.py createsuperuser

## Contribute to the project

### Create local copy of the branch you want to work on:

git checkout -b name_of_the_branch origin/name_of_the_branch

### Work on the branch, save, commit and push changes to remote repository.

git status

(checks the status of git repository)###

git add *

(adds all changes to the staging area)

git commit -m "Your commit message"

(commits changes in the local repository)

git push -u origin name_of_branch


# Test github actions.






















