# Django RestFramework Swagger Master

## Summary
* Django
* Django Environ
* Django Template
* Django RestFramework
* Django RestFramework Swagger

Save your time and please PR if more feature for django template.

## Environment
1. Install Server Firewall
    > sudo ufw enable
    > sudo ufw allow ssh
    > sudo ufw allow http
    > sudo ufw allow https
    > sudo ufw allow ftp
    > sudo ufw status
2. Install Python Environment
    > sudo apt-get install python3-dev virtualenv 
3. Install Database Service
    Mysql
    - install
    > sudo apt-get install build-essential mysql-server libmysqlclient-dev
    
    - service
    > sudo ufw allow mysql
    > sudo systemctl start mysql
    > sudo systemctl enable mysql

    - setting root user
    > sudo -u root mysql

    > USE mysql;
    > UPDATE user SET authentication_string=PASSWORD("rootpassword") WHERE User='root';
    > UPDATE user SET plugin="mysql_native_password";
    > FLUSH PRIVILEGES;
    > exit

    - setting new user
    > CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
    > GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'localhost';
    > FLUSH PRIVILEGES;
    > exit

    > mysql -u myuser -p

    > CREATE DATABASE mydb;
    
    Postgresql
    - install
    > sudo apt-get install libpq-dev postgresql postgresql-contrib

    - service
    > sudo ufw allow postgresql
    > sudo systemctl start postgresql
    > sudo systemctl enable postgresql

    - setting root user
    > sudo -u postgres psql
    > \password sde
    > \q
    
    - setting new user
    > CREATE DATABASE mydb;

    > CREATE USER myuser WITH PASSWORD 'mypassword';
    > ALTER ROLE myuser SET client_encoding TO 'utf8';
    > ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
    > ALTER ROLE myuser SET timezone TO 'UTC';
    > GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;

## Installation
4. Install [Django Project](https://docs.djangoproject.com/en/3.0/topics/install/)
    - setting secret key 
    > mv mysite/_secret_settings.py mysite/secret_settings.py
    > nano mysite/secret_settings.py

    - install virtual environment
    > virtualenv -p python3 venv
    > source venv/bin/activate

    - install django project
    > pip install -r requirement.txt
    > python manage.py makemigrations
    > python manage.py migrate
    > python manage.py createsuperuser
    > python manage.py collectstatic

    - testing django project
    > sudo ufw allow 8000
    > python manage.py runserver 0:8000

## Deployment
5. Install Gunicorn
    > pip install gunicorn
    > gunicorn --bind 0.0.0.0:8000 mysite.wsgi

    > sudo nano /etc/systemd/system/gunicorn.service

    ```
    [Unit]
    Description=gunicorn daemon
    After=network.target
    
    [Service]
    User=ubuntu
    Group=www-data
    WorkingDirectory=/home/ubuntu/mysite
    ExecStart=/home/ubuntu/django-rest-swagger-master/mysite/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/ubuntu/mysite/mysite.sock mysite.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
    ```
    
    > sudo systemctl restart gunicorn
    > sudo systemctl enable gunicorn
6. Install Nginx
    > sudo apt-get install nginx
    > sudo nano /etc/nginx/sites-available/mysite

    ```
    server {
        listen 80;
        server_name server_domain_or_IP;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /home/ubuntu/django-rest-swagger-master;
        }
        location /static/ {
            root /home/ubuntu/django-rest-swagger-master;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/home/ubuntu/django-rest-swagger-master/mysite.sock;
        }
    }
    ```
    > sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled
    > sudo nginx -t
    > sudo systemctl restart nginx
    > sudo ufw allow 'Nginx Full'

