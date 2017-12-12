# pitchfork
Project Pitchfork
Most of our code is selfdocumented. We followed the basic "django style".
Steps to get running:

Make sure you have some sort of working python 3. It needs to have pip / brew / cygwin-apt.

Reqs: NOTE: We have had lots of issues setting this up on different environments. Looking back, we really should have used a virtual-env.

Run "pip install -r requirements.txt" or "pip3 install -r requirements.txt"

Start MySQL server locally or ssh into it.
First run on new DB: Run "python manage.py migrate" or "python3 manage.py migrate"

Admin:
Create superuser with
 Run "python manage.py createsuperuser" or "python3 manage.py createsuperuser"
    Login to admin panel at http://localhost:8000/admin/


Running Server:
   Run "python manage.py runserver 8000" or "python3 manage.py runserver 8000"

   Connect via http://localhost:8000 ( no HTTPS support atm )

Create groups via the admin panel.
Items can be added through either interface.
Users still need to be added to groups.


BASIC STRUCTURE:
base.html : contains template information used throughout the site.
models.py : the way we store our data
views.py  : the way we access our data and render html pages.
urls.py   : the way urls link to views.
admin.py  : used for admin

TODO:
Group creation and Ownership, Item management on frontend, email functionality.  
