
### Installation ###

## Linux

To run this application on linux in local you need python3.7, pip and virtalenv.

### Python, pip and virtualenv

Steps for installing:

sudo apt install python3.8

restart terminal

### Install pip - library for downloading python modules:

sudo apt install python3-pip   

(type pip3 command to check if pip is installed)  

### Install venv - library for creating virtual environments:

sudo apt install python3-venv 

### Create a project folder:

mkdir zajednica

### Enter this folder:

cd zajednica

### Clone project from github:

git clone https://github.com/Matje1979/zajednicastanara.git

### Create venv (virtual environment) named django_env (can use other name) in the folder:

/usr/bin/python3.8 -m venv django_env

### Activate venv:

source django_env/bin/activate

### Check final steps bellow

## Windows

### Python

Go to https://www.python.org/downloads/

Find python version 3.8 (any more specific version)

Click download

Click on downloaded .exe file.

Python installer will open. Check Add Python 3.8 to PATH checkbox.

Click Customize Installation

In Optional Features check all, and click next.

In Advanced Options change location for python installation (totally optional)

Click install

### Install virtualenv

pip3 install virtualenv 

### Create a project folder:

mkdir zajednica

### Enter this folder:

cd zajednica

### Clone project from github:

git clone https://github.com/Matje1979/zajednicastanara.git

### Create venv (virtual environment) named django_env (can use other name) in the folder:

virtualenv --python C:\Path\To\Python\python.exe django_env

### Activate venv:

.\django_env\Scripts\activate

# Final steps
(same for Windows and Linux)

### Installing dependencies:

pip3 install -r home_manager/requirements.txt

### Run project:

cd home_manager

python3 manage.py runserver

Check website at localhost:8000

## Settings

Go to home_manager/settings.py

Replace WSGI_APPLICATION = 'zajednicastanara.wsgi.application' with WSGI_APPLICATION = 'home_manager.wsgi.application'.

Replace Debug = False with Debug = True

cors_allowed_headers and cors_allow_all_origins as well as rest_framework = {} put in comments.

Set allowed hosts to []. Allowed_hosts = [ ]

Uncomment STATICFILES_DIRS line

Comment out lines STATIC_ROOT and MEDIA_ROOT lines.

























