# pitchfork
Project Pitchfork
Most of our code is selfdocumented. We followed the basic "django style".
Steps to get running:

Make sure you have some sort of working python 3. It needs to have pip / brew / cygwin-apt.

Reqs:
Run "pip install -r requirements.txt" or "pip3 install -r requirements.txt"

Start MySQL server locally or ssh into it.
First run on new DB: Run "python manage.py migrate" or "python3 manage.py migrate"

Running Server:
 Run "python manage.py runserver 8000" or "python3 manage.py runserver 8000"

 Connect via http://localhost:8000 ( no HTTPS support atm )

Admin:
Create superuser with
 Run "python manage.py createsuperuser" or "python3 manage.py createsuperuser"
    Login to admin panel at http://localhost:8000/admin/
