# Catalog App
[http://clappaws.club/](http://clappaws.club/)  [http://34.214.27.203/](http://34.214.27.203/)

Catalog app is a small restful CRUD app with python flask and postgresql sqlalchemy deploying on
apache2 server hosted on AWS lightsail ubuntu 16.04 LTS. This app is to display sport equipments categories and items
to the general public, and allow authorized users to create, update, and delete categories and items.

## Technical Features

- Apache2
- Ubuntu 16.04 on AWS lightsail
- VirtualEnv
- Virtualbox and Vagrant
- Python 3.5/3.6  
- Twitter Bootstrap 4
- Coverage and Tox *(cross-platform cross-version test tools)*
- Flask Framework
- Mod_WSGI
- Flask Login
- Flask OAuthlib 
- Flask WTForms *(validate form elements)*
- Flask Flash *(display flash messages)*
- Flash SQLAlchemy 
- Postgresql
- SQLAlchemy
- Psycopg2
- Jinja2
- Werkzeug
- Ratelimit
- Decorator
- Requests
- Oauthlib
- Itsdangerous
- MarkupSafe
- Pep8

## Functional Features 

- Create blueprints to distribute a large app into resuable components
- Utilize restful CRUD to create/update/delete categories and items records by authoirzed users 
- Employ authentication and authorization to grant CRUD access to authorized users
- Generate catalog.json endpoint at *http://<host>/catalog.json*
- Add a new database user "catalog" with limited permission (CreateDB only)

## Configuration Features

- Change ssh port from 22 to 2200
- Configure the Uncomplicated Firewall (UFW) to only allow incoming connections for SSH (port 2200), 
HTTP (port 80), and NTP (port 123)
- Assign a new user "grader" the permission to access apache server on AWS lightsail

## Steps of Installation and Configuration on Virtual Machine
### 1. Install Virtualbox
- Download virtual box from *https://www.virtualbox.org/wiki/Download_Old_Builds_5_1*
- Follow the instructions to setup virtualbox

### 2. Install Vagrant
- Download vagrant from *https://www.vagrantup.com/downloads*
- Follow the instructions to setup vagrant.  *(Note: if the current version is non-compatiable with your OS,
downgrade the version)*

### 3. Configure Virtual Machine Environment
- Download from *https://github.com/udacity/fullstack-nanodegree-vm*
- Download source codes from *https://github.com/melc/catalog*

    ```
    cd fullstack-nanodegree-vm/vagrant
    cd catalog
    git clone https://github.com/melc/catalog
    ```
- Install ubuntu 16.04 LTS

    ```
    cd vagrant/
    vagrant up
    ```
- Login to installed ubuntu VM

    `vagrant ssh`     *(note: $ will be changed to vagrant@vagrant:~$)*

### 5. Launch the Application
- Launch run.py

    `python3.5 run.py`


## Steps of Installation and Configuration on Apache with AWS Lightsail Ubuntu 16.04 LTS
### 1. Set up AWS Lightsail
- Create an account on *http://aws.amazon.com*
- On AWS Managament Console select Lightsail
- Choose OS only Ubuntu 16.04 LTS
- Change SSH key pair from default to a new ssh key pairs and download to your local machine
- Create Instance and Static IP, attach static ip to instance

### 2. Configure the Firewall (Change ssh port from 22 to 2200)
- Open the file /etc/ssh/sshd_config on local machine, change the port number 22 to 2200.
- Click on the button "Connect using SSH", and execute the following commands on remote machine
    ```
    sudo service ssh restart
    sudo ufw status
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow ssh
    sudo ufw allow 2200/tcp
    sudo ufw allow www
    sudo ufw allow 123/udp
    sudo ufw deny 22
    sudo ufw enable
    sudo ufw status
    ```
  
    To | Action | From
    --- | --- | ---
    22 | DENY | Anywhere
    2200/tcp | ALLOW | Anywhere
    80/tcp | ALLOW | Anywhere
    123/udp | ALLOW | Anywhere
    22 (v6) | ALLOW | Anywhere
    2200/tcp (v6) | ALLOW | Anywhere (v6)
    80/tcp (v6) | ALLOW | Anywhere (v6)
    123/udp (v6) | ALLOW | Anywhere (v6)

- Update external firewall by clicking on the AWS lightsail instance, then selecting the 'Networking' 
tab, and configuring the firewall to match the internal firewall settings above (123(UDP) and 
2200(TCP));
- Change the permission of ssh key pairs file to readonly on local machine

    `chmod 600 </path/to/ssh key pairs>.pem`

- Logon remote machine

    `ssh -i </path/to/ssh key pairs>.pem -p 2200 ubuntu@<aws lightsail public ip>`

### 3. Create New User *grader* With `sudo` Permission on Remote Machine
- Create a new user *grader*

    `sudo adduser grader`
- Enter passphrase twice
- Check if the new user was created successfully

    `su - grader`       (the user should be changed from ubuntu to grader)
- Grant *sudo* permission to the new user

    `sudo visudo`       (make sure the user is ubuntu in lieu of grader)

    Insert the following line of codes under `root ALL=(ALL:ALL) ALL`

    `grader ALL=(ALL:ALL) ALL`
- Verify the new user having *sudo* permission

    `su - grader`

    `sudo -l`

    > Matching Defaults entries for grader on

    > ip-XX-XX-XX-XX.ec2.internal:

    > env_reset, mail_badpass,

    > secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

    > User <new user> may run the following commands on

    >   ip-XX-XX-XX-XX.ec2.internal:

    >   (ALL : ALL) ALL

### 4. Logon Remote Machine With The New User *grader*
- On local machine,
    - Execute the following:

        `<path/to/ssh-keygen>/ssh-keygen`
    - Choose a file name for the ssh key pair   *(ex. grader_key)*
        - Enter passphrase twice
        - Copy the contents of ssh key pair file    *(ex. grader_key.pub)*

            `cat / <path/to/ssh-keygen> grader_key.pub`
        - Log in to the remote machine

            ` ssh -i </path/to/ssh key pairs>.pem -p 2200 ubuntu@<aws lightsail public ip>`
- On remote machine,
    - Switch to the new user grader home directory

        `su - grader`
    - Create a new directory .ssh

        `sudo mkdir .ssh`
    - Create a new file authorized_keys

        `touch ~/.ssh/authorized_keys`
    - Paste the contents of ssh key pair file into authorized_keys
        - Change .ssh and authorized_keys permissions.
        ```
        chmod 700 .ssh
        chmod 644 .ssh/authorized_keys
        ```
        - Check PasswordAuthentication setting
            open the file /etc/ssh/sshd_config, and find the following line,
        ```
        # Change to no to disable tunnelled clear text passwords
        'PasswordAuthentication  'no'
        ```
- On local machine,
    - login to remote machine with the new user "grader"

    `ssh -i <ssh key pair> -p 2200 <new user>@<aws lightsail public ip>`   *(ex. grader_key)*

### 5. Set The Local Timezone to UTC on Remote Machine
- Execute the following command,

    `sudo dpkg-reconfigure tzdata`
- Go to bottom, and select “None of the above”
- Select "UTC"

### 6. Install Apache2, Python3.5, and Mod_Wsgi on Remote Machine
- Install apache2,

    ```
    sudo apt-get update
    sudo apt-get install apache2 apache2-dev
    ```
- Install python3.5

    `sudo apt-get install python3.5-dev`
- Install mod wsgi

    `sudo apt-get install libapache2-mod-wsgi-py3`
- Update and upgrade packages

    `sudo apt-get update && sudo apt-get upgrade`
- Enable apache module, mod wsgi, and restart apache
    ```
    sudo a2enmod wsgi		                *****  enabling module wsgi
    sudo service apache2 restart            *****  activate the new configuration
    ```

### 7. Install and Start Postgresql on Remote Machine
- Install postgresql

    `sudo apt-get install postgresql postgresql-contrib`
- Start postgresql

    `sudo /etc/init.d/postgresql start`

### 8. Create Database *catalog* and Assign its Ownership to Superuser *vagrant*
- Create a database superuser *vagrant*

    ```
    sudo -u postgres -i
    psql
    CREATE ROLE vagrant WITH LOGIN;
    ALTER ROLE vagrant with ENCRYPTED PASSWORD 'vagrant';
    ```
- Create database catalog with superuser owner *vagrant*

    ```
    CREATE DATABASE catalog OWNER 'vagrant';
    ALTER ROLE vagrant SUPERUSER;
    ```
- Insert the following line of codes into the file /etc/postgresql/9.5/main/pg_hba.conf

    ```
    local       all             vagrant                 peer
    ```

### 9. Create Postgresql User With Limited Permissions
- Create a database user *catalog*

    ```
    sudo /etc/init.d/postgresql restart
    sudo -u postgres -i
    psql
    CREATE USER catalog WITH LOGIN;
    ALTER ROLE catalog with ENCRYPTED PASSWORD 'catalog';
    ```
- Assign create database permission to new user *catalog*

    `ALTER ROLE catalog WITH CREATEDB;`
- Insert the following line of codes into the file */etc/postgresql/9.5/main/pg_hba.conf*

   `local    all             	<db user name>                                md5`
- Restart postgresql

    `sudo /etc/init.d/postgresql restart`

### 10. Download Catalog Source Codes From Github, Set up Virtual Environment, and Install Dependencies
- Download project catalog from github

    ```
    cd /var/www/
    git clone https://github.com/melc/catalog
    ```
- Change ownership of catalog to ubuntu

    `sudo chown -R ubuntu:ubuntu /var/www/catalog`
- Install virtualenv

    ```
    apt-get install python3-pip
    pip3 install virtualenv
    ```
- Create virtual environment for catalog app

    ```
    cd /var/www/catalog
    virtualenv -p python3.5 venv
    ```
- Activate virtual environment

    `source venv/bin/activate`
- Install python3.5 dependencies

    `venv/bin/python3.5 -m pip install -r requirements.txt`
- Check if dependencies installed correctly

    `cd venv/lib/python3.5/site-packages`
- Run catalog application on default localhost *http://127.0.0.1:5000/*

    `python3.5 run.py`
- Deactivate virtual environment

    `deactivate`

### 11. Set Environment Variables Being Used in Catalog App
- Create a file *config.py*

    `touch /var/www/catalog/config.py`
- Copy the following lines of codes and paste to the file *config.py*
    ```
    import os

    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(20)
    GOOGLE_CLIENT_ID = <google client_id>
    GOOGLE_CLIENT_SECRET = <google client secret>
    FACEBOOK_APP_ID = <facebook app id>
    FACEBOOK_APP_SECRET = <facebook app secret>
    SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost:5432/catalog'
    ```

### 12. Setup Google and Facebook API accounts
- Setup google api account
    - Go to google deveoper console, *https://console.developers.google.com/apis/dashboard*
    - Select credentials, create Client ID and Client Secret
    - Copy Client ID and Client Secret to the file *config.py*
    - Setup authorized javascript origins *(ex. http://127.0.0.1:5000)*
    - Setup authorized redirect URIs  *(ex. http://127.0.0.1:5000/login/google_authorized)
- Setup facebook api account
    - Go to facebook graph api console, *https://developers.facebook.com/*
    - Choose facebook login, click on `My Apps` on top right screen, select `Add a New App`
    - Follow the instruction to create APP ID and APP SECRET
    - Copy APP ID and APP SECRET to the file *config.py*
    - Select facebook login dashboard, set `Client OAuth Login` to `Yes`, `Web OAuth Login` to `Yes`
    - Setup valid oauth redirect URIs  *(ex. http://127.0.0.1:5000/login/facebook_authorized)*

### 13.  Configure virtual host
- Configure virtual host

    ```
    touch  /etc/apache2/sites-available/catalog.conf
    copy and paste the following lines of codes into the file *catalog.conf*
    ```
    ```
    <VirtualHost *:80>
        ServerName XX.XX.XX.XX
        ServerAdmin xxx@gmail.com
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/webapp/>
            Order allow,deny
            Allow from all
            Options -Indexes
        </Directory>
        Alias /static /var/www/catalog/webapp/static

        <Directory /var/www/catalog/webapp/static>
            Order allow,deny
            Allow from all
            Options -Indexes
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
    </VirtualHost>
    ```
- Enable virtual host

    ```
    a2dissite 000-default					*** disable default configuration file
    sudo a2ensite catalog					*** enable new created configuration file
    sudo service apache2 restart
    sudo apache2ctl restart
    ```

### 14. Configure .wsgi file
- Create .wsgi file */var/www/catalog/catalog.wsgi*
- Add the following lines of codes into the file *catalog.wsgi*

    ```
    #!/usr/bin/python
    activator = '/var/www/catalog/venv/bin/activate_this.py'
    # Looted from virtualenv; should not require modification, since it's defined relatively

    with open(activator) as f:
        exec(f.read(), {'__file__': activator})

    import sys
    import logging

    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/catalog/")

    from run import app  as application
    ```

- Restart apache

    `sudo service apache2 restart`

***
![Catalog App Home Page](http://clappaws.club/catalog.png)