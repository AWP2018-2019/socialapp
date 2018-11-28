# socialapp
An example socialapp 

How to create a new project and app in Django:

    pip install django=1.11
    # Create project
    django-admin.py startproject [project_name] [path]
    Ex: django-admin.py startproject socialapp .
    # Create app
    python manage.py app

Install virtualenv:
        
        virtualenv venv
        . venv/bin/activate

Install packages:
        
        pip install -r requirements.txt
        
Apply migrations:
        
        python manage.py migrate
        
Create migrations:
        
        python manage.py makemigrations
        
Start server:
        
        python manage.py runserver $IP:$PORT