COMP 3005 Fall 2025
Cal McLelland
Final Project

----------------------------------------------
-- Installation (Windows PowerShell w/ WSL) --
----------------------------------------------

---------
-- WSL --
---------

wsl --install

------------
-- Python --
------------

wsl -u \<username\>

sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential libpq-dev

-- create a virtual environment with venv

python3 -m venv .venv
source .venv/bin/activate

----------------
-- SQLAcademy --
----------------

python -m pip install --upgrade pip setuptools wheel
python -m pip install sqlalchemy psycopg[binary] psycopg2-binary

-------------------------------
-- Create Database (pgadmin) --
-------------------------------

In pgAdmin 4 (install instructions) create a new postgres database called "student"


Link to Demo Video

https://mediaspace.carleton.ca/media/Cal_McLelland_Final_Project_demo_COMP3005/1_qzntrypw

