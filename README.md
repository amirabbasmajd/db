### Description
Enceladus - is a microblogging platform using Flask and MongoDB.

![alt text](https://raw.githubusercontent.com/lk-geimfari/enceladus/master/screenshots/main_after_signed_in.png)

###Usage
For first you must do is create virtual environment and activate it:
```zsh
➜  ~  virtualenv -p /usr/bin/python3.4 venv
➜  ~  source venv/bin/activate
```

or if you use virtualenvrapper:
```zsh
➜  ~ mkvirtualenv venv
➜  ~ workon venv
```

After virtual environment is created and activated you need install all requirements using pip (or another python package manager):
```zsh
(venv) ➜ ~ pip install -r requirements.txt
```

Finally you must export environment variables:
```zsh
export FLASK_CONFIG = "config_name"

export SECRET_KEY = "your_secret_key"
export FLASK_MONGO_DB = "enceladus_db"

export MAIL_USERNAME = "email@example.com"
export MAIL_PASSWORD = "password"
```

#####If you use .secret_key file then never do not forget add a .secret_key to the .gitignore.

###Run
```
(venv) ➜ ~ python3 enceladus/manage.py runserver
```

###Structure
```
enceladus
├── app
│   ├── api_1_0
│   │   └── __init__.py
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── decorator.py
│   ├── email.py
│   ├── errors.py
│   ├── __init__.py
│   ├── main
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   └── views.py
│   ├── static
│   │   ├── css
│   │   │   ├── bootstrap.css
│   │   │   ├── bootstrap.min.css
│   │   │   ├── profile.css
│   │   │   ├── simple-style.css
│   │   │   ├── site.css
│   │   │   └── site.min.css
│   │   ├── fonts
│   │   │   ├── glyphicons-halflings-regular.eot
│   │   │   ├── glyphicons-halflings-regular.svg
│   │   │   ├── glyphicons-halflings-regular.ttf
│   │   │   ├── glyphicons-halflings-regular.woff
│   │   │   └── glyphicons-halflings-regular.woff2
│   │   ├── img
│   │   │   └── wow.png
│   │   └── js
│   │       ├── alert.js
│   │       ├── bootstrap.js
│   │       ├── bootstrap.min.js
│   │       ├── jquery.js
│   │       └── site.min.js
│   ├── templates
│   │   ├── add_post.html
│   │   ├── auth
│   │   │   ├── login.html
│   │   │   └── registration.html
│   │   ├── email
│   │   │   └── message.html
│   │   ├── errors
│   │   │   ├── 400.html
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── flash.html
│   │   ├── index.html
│   │   ├── layout.html
│   │   └── profile.html
│   └── user.py
├── config.py
├── manage.py
├── README.md
├── requirements.txt
├── runtime.txt
├── screenshots
│   ├── add_post.png
│   ├── main_after_signed_in.png
│   ├── main.png
│   ├── sign_up.png
│   └── user_profile.png
└── test_basic.py


```

###TODO
1. Add comments
2. Add user profiles
3. Add search
4. Add tests
5. Add Dockerfile
6. Add API

###Runtime
Python 3.4.3
