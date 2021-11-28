# ZajednicaStanara

### Installation ###

(Install git before following bellow instructions)

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

### Install requirements:

pip3 install -r home_manager/requirements.txt

# Contribute to the project

### Create local copy of the branch you want to work on:

git checkout -b name_of_the_branch origin/name_of_the_branch

### Work on the branch, save, commit and push changes to remote repository. 

git status

(checks the status of git repository)

git add *

(adds all changes to the staging area)

git commit -m "Your commit message"

(commits changes in localk repository)

git push -u origin name_of_branch

(pushes changes to remote)




















