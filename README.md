# Catalog App
[http://clappaws.club/](http://clappaws.club/)   
[http://34.214.27.203/](http://34.214.27.203/)

Catalog app is a small restful CRUD app with python flask and postgresql sqlalchemy 
deploying on apache2 server hosted on AWS lightsail ubuntu 16.04 LTS. This app is to 
display sport equipments categories and items to the general public, and 
allow authorized users to create and update categories and items, and delete items.

## Technical Features

- Apache2
- Ubuntu 16.04 on AWS lightsail
- VirtualEnv
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
- Virtualbox and Vagrant

## Functional Features 

- Create blueprints to distribute a large app into reusable components
- Utilize restful CRUD to create/update/delete categories and items records 
by authoirzed users 
- Employ authentication and authorization to grant CRUD access to authorized users
- Generate catalog.json endpoint at *http://<host>/catalog.json*
- Add a new database user "catalog" with limited permission (CreateDB only)

## Configuration Features

- Change ssh port from 22 to 2200
- Configure the Uncomplicated Firewall (UFW) to only allow incoming connections 
for SSH (port 2200), 
HTTP (port 80), and NTP (port 123)
- Assign a new user "grader" the permission to access apache server on AWS lightsail

## Installation and Configuration on Virtual Machine
### 1. Install Virtualbox
- Download virtual box from *https://www.virtualbox.org/wiki/Download_Old_Builds_5_1*
- Follow the instructions to setup virtualbox

### 2. Install Git
- Download git from *https://git-scm.com/downloads*
- follow the instructions to set up git bash 

### 3. Install Vagrant
- Download old version of vagrant from *https://www.vagrantup.com/downloads* if 
the current version is non-compatiable with your OS. 
- Follow the instructions to setup vagrant.  

### 4. Download Vagrantfile and Source Codes
- Create a folder *vagrant*
- Download *vagrantfile* from *https://github.com/udacity/fullstack-nanodegree-vm*
to the folder vagrant
- Git clone from *https://github.com/melc/catalog* to the folder vagrant

    ```
    cd /vagrant
    git clone https://github.com/melc/catalog
    ```
- Createa a new file *config.py* in the folder catalog, copy the following lines of 
codes and paste to the file *config.py*, insert your values.
   
    ```
    import os

    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(20)
    GOOGLE_CLIENT_ID = 
    GOOGLE_CLIENT_SECRET = 
    FACEBOOK_APP_ID = 
    FACEBOOK_APP_SECRET = 
    SQLALCHEMY_DATABASE_URI = 'postgresql://<user name>:<password>@localhost:5432/catalog'
    ```

### 5. Configure Virtual Machine
- Install ubuntu 16.04 LTS

    ```
    cd /vagrant
    vagrant up   
    ```
- Logon installed ubuntu VM

    `vagrant ssh`     *(note: $ will be changed to vagrant@vagrant:~$)*

### 6. Launch the Application
- Install python dependencies
    
    `sudo python3.5 -m pip install -r requirements.txt`
    
- Create database *catalog*
    
    ```
    psql
    CREATE DATABASE catalog;
    ```
- Replace line of code in the file *application.py*, 
    
    ```
    old code: app.run(debug=True)
    
    new code: app.run(debug=True, host='0.0.0.0', port=8000)
    ```
- Replace line of code in the file *catalog/webapp/app.py*
    
    ```
    old code: app.config.from_pyfile('/var/www/catalog/config.py')
    
    new code: app.config.from_object('config')
    ```    
- Launch application.py

    `python3.5 application.py`

- Open browser and type in `localhost:8000`


## Installation and Configuration on Apache With AWS Lightsail Ubuntu 16.04 LTS
### 1. Set up AWS Lightsail
- Create an account on *http://aws.amazon.com*
- On AWS Managament Console select *Lightsail*
- Choose *OS only* and *Ubuntu 16.04 LTS*
- Create a new SSH key pairs in lieu of default one and download to your host machine
with the file extension .pem
- Create *Instance* and *Static IP*, attach static ip to instance

### 2. Configure the Firewall (Change ssh port from 22 to 2200)
- Open the file */etc/ssh/sshd_config* on virtual machine, change the port number 22 to 2200.
- On AWS lightsail main page, click on the button *Connect using SSH*, and execute 
the following commands on virtual machine
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

- Click on *Networking" tab on AWS lightsail main page to update firewall information.
Add custom TCP port 2200, and custom UDP port 123
- Change the permission of ssh key file on host machine

    `chmod 600 </path/to/ssh key file with file extension .pem>`

- Logon virtual machine

    `ssh -i </path/to/ssh key file with file extension .pem> -p 2200 
    ubuntu@<aws lightsail public ip>`

### 3. Create New User *grader* With `sudo` Permission on Virtual Machine
- Create a new user *grader*

    `sudo adduser grader`
- Enter passphrase twice
- Check if the new user was created successfully

    `su - grader`       *(note: the user should be changed from ubuntu to grader)*
- Grant *sudo* permission to the new user

    ```
    exit
    sudo visudo       *(note: make sure the user is ubuntu)*
    ```
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

### 4. Logon Virtual Machine With The New User *grader*
- On host machine,
    - Execute the following command to generate private and public SSH key pairs

        `<path/to/ssh-keygen>/ssh-keygen`
    - Choose a file name for the ssh key pairs   *(ex. grader_key as private key and
    grader_key.pub as public key)*
    - Enter passphrase twice 
    - Logon to the virtual machine with the user *ubuntu*

        ` ssh -i </path/to/ssh key file with the file extention .pem> -p 2200 
        ubuntu@<aws lightsail public ip>`
- On virtual machine,
    - Switch to the new user *grader* home directory

        `su - grader`
    - Create a new directory *.ssh*

        `sudo mkdir .ssh`
    - Create a new file authorized_keys

        `touch ~/.ssh/authorized_keys`
    - Copy the contents in the public ssh key file (ex. *grader_key.pub*) on host machine and 
    paste to the file *authorized_keys*

        `cat / <path/to/ssh-keygen> grader_key.pub`
    - Change *.ssh* and *authorized_keys* permissions.
        
        ```
        chmod 700 .ssh
        chmod 644 .ssh/authorized_keys
        ```
    - Check PasswordAuthentication setting
        open the file */etc/ssh/sshd_config*, and find the following line,
        
        ```
        # Change to no to disable tunnelled clear text passwords
        'PasswordAuthentication  'no'
        ```
- On host machine,
    - logon virtual machine with the new user *grader*

        `ssh -i <private ssh key pair> -p 2200 <new user>@<aws lightsail public ip>`   
    *(ex. grader_key)*

### 5. Set The Local Timezone to UTC on Virtual Machine
- Execute the following command,

    `sudo dpkg-reconfigure tzdata`
- Go to bottom, and select *None of the above*
- Select *UTC*

### 6. Install Apache2, Python3.5, and Mod_Wsgi on Virtual Machine
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

### 7. Install and Start Postgresql on Virtual Machine
- Install postgresql

    `sudo apt-get install postgresql postgresql-contrib`
- Start postgresql

    `sudo /etc/init.d/postgresql start`

### 8. Create Database *catalog* and Assign its Ownership to Superuser *vagrant*
- Create a database user *vagrant*

    ```
    sudo -u postgres -i
    psql
    CREATE ROLE vagrant WITH LOGIN;
    ALTER ROLE vagrant with ENCRYPTED PASSWORD 'vagrant';
    ```
- Create database *catalog* with superuser owner *vagrant*

    ```
    CREATE DATABASE catalog OWNER 'vagrant';
    ALTER ROLE vagrant SUPERUSER;
    ```
- Insert the following line of codes into the file */etc/postgresql/9.5/main/pg_hba.conf*
    
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
- Insert the following line of codes into the file */etc/postgresql/9.5/main/pg_hba.conf*.  
Replace *db user name* with your database user name  *(ex. catalog)*

   `local    all             	<db user name>                                md5`
- Restart postgresql

    `sudo /etc/init.d/postgresql restart`

### 10. Git Clone Source Codes, Set up Virtual Environment, and Install Dependencies
- Git clone source codes

    ```
    cd /var/www/
    git clone https://github.com/melc/catalog
    ```
- Change file ownership of *catalog* package to ubuntu

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
- Run *catalog* application to make sure application working properly

    ```
    python3.5 application.py
    go to browser and type in *http://localhost:8000/*
    ```
- Deactivate virtual environment

    `deactivate`

### 11. Create Configuration File
- Createa a new file *config.py* in the folder */var/www/catalog*, 
copy the following lines of codes and paste into the file *config.py*, insert your values.
   
    ```
    import os

    DEBUG = True
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(20)
    GOOGLE_CLIENT_ID = 
    GOOGLE_CLIENT_SECRET = 
    FACEBOOK_APP_ID = 
    FACEBOOK_APP_SECRET = 
    SQLALCHEMY_DATABASE_URI = 'postgresql://<user name>:<password>@localhost:5432/catalog'
    ```

### 12. Setup Google and Facebook API accounts
- Setup google api account
    - Go to google developer console, *https://console.developers.google.com/apis/dashboard*
    - Select credentials, create Client ID and Client Secret
    - Copy Client ID and Client Secret, and paste to the file *config.py*
    - Setup `authorized javascript origins`   *(ex. http://127.0.0.1:5000)*
    - Setup `authorized redirect URIs`   *(ex. http://127.0.0.1:5000/login/google_authorized)
- Setup facebook api account
    - Go to facebook graph api console, *https://developers.facebook.com/*
    - Choose product *facebook login*, click on `My Apps` on top right screen, 
    select `Add a New App`
    - Follow the instruction to create APP ID and APP SECRET
    - Copy APP ID and APP SECRET, paste to the file *config.py*
    - Select facebook login dashboard, set `Client OAuth Login` to `Yes`, 
    `Web OAuth Login` to `Yes`
    - Setup `valid oauth redirect URIs`  *(ex. http://127.0.0.1:5000/login/facebook_authorized)*

### 13.  Configure Virtual Host
- Create a new file *catalog.conf*
- Copy the following lines of codes and paste into the file *catalog.conf*

    ```
    <VirtualHost *:80>
        ServerName XX.XX.XX.XX
        ServerAdmin xxx@gmail.com
        
        WSGIScriptAlias / /var/www/catalog/catalog.wsgi
        <Directory /var/www/catalog/webapp/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/catalog/webapp/static

        <Directory /var/www/catalog/webapp/static>
            Order allow,deny
            Allow from all
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
    ```

### 14. Configure WSGI
- Create WSGI file */var/www/catalog/catalog.wsgi*
- Add the following lines of codes into the file *catalog.wsgi*

    ```
    #!/usr/bin/env python3.5
    activator = '/var/www/catalog/venv/bin/activate_this.py'

    # Looted from virtualenv; should not require modification, 
    since it's defined relatively

    with open(activator) as f:
        exec(f.read(), {'__file__': activator})

    import sys
    import logging

    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/catalog/")

    from run import app as application
    ```

- Restart apache

    `sudo service apache2 restart`

***
![Catalog App Home Page](http://clappaws.club/static/img/catalog.png)