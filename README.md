# socialapp
An example socialapp 


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