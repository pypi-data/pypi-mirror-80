# django-server-controller

Django server controllers, e.g. UwsgiController, GunicornController.

## Install

```shell
pip install django-server-controller
```

## Django Command Help

```
C:\Workspace\my_django_project>python manage.py wsgi-server --help
Usage: manage.py wsgi-server [OPTIONS] COMMAND [ARGS]...

Options:
  --version                      Show the version and exit.
  -h, --help                     Show this message and exit.
  -v, --verbosity INTEGER RANGE  Verbosity level; 0=minimal output, 1=normal
                                 output, 2=verbose output, 3=very verbose
                                 output.

  --settings SETTINGS            The Python path to a settings module, e.g.
                                 "myproject.settings.main". If this is not
                                 provided, the DJANGO_SETTINGS_MODULE
                                 environment variable will be used.

  --pythonpath PYTHONPATH        A directory to add to the Python path, e.g.
                                 "/home/djangoprojects/myproject".

  --traceback / --no-traceback   Raise on CommandError exceptions.
  --color / --no-color           Enable or disable output colorization.
                                 Default is to autodetect the best behavior.


Commands:
  reload   Reload uwsgi server.
  restart  Restart uwsgi server.
  start    Start uwsgi server.
  status   Get uwsgi server's status.
  stop     Stop uwsgi server.
```

## Usage

**pro/settings.py**

```
INSTALLED_APPS = [
    ...
    'django_server_controller',
    ...
]

WSGI_SERVER_ENGINE = "uwsgi"   # required. uwsgi or gunicorn, default to uwsgi.

WSGI_PROJECT_NAME = xxx # used for name of the default pidfile
WSGI_PROJECT_BASE = xxx
WSGI_WEB_ROOT = xxx # chdir to web root before starting server
WSGI_LOGS_ROOT = xxx
WSGI_PIDFILE = xxx
WSGI_CONFIG_FILE = xxx
WSGI_BIN = xxx
KILL_BIN = xxx # used for send signal to gunicorn process, no use for uwsgi

```

- Add django_server_controller into INSTALLED_APPS, so that we can use it's django-management-commands.
- You can add server settings in django's settings.py. If not provide, the default values are used.
- UWSGI_PROJECT_BASE defaults to current directory. *Suggest you set this variable*.
- CONFIG_FILE search orders for uwsgi server engine:
    1. settings.CONFIG_FILE pointed file.
    1. settings.WSGI_PROJECT_BASE + "./etc/wsgi.ini"
    1. ./etc/wsgi.ini
    1. ~/etc/wsgi.ini
    1. python-lib-root/lib/python3.6/site-packages/the_project_package/wsgi.ini
- CONFIG_FILE search orders for gunicorn server engine:
    1. settings.CONFIG_FILE pointed file.
    1. settings.WSGI_PROJECT_BASE + "./etc/wsgi.conf.py"
    1. ./etc/wsgi.conf.py
    1. ~/etc/wsgi.conf.py
    1. python-lib-root/lib/python3.6/site-packages/the_project_package/wsgi.conf.py


## Suggest project folders

```
./bin/
./etc/
./lib/
./lib64/
./web/
./web/static/
./web/upload/
./logs/
```

- suggest you use virtualenv.
- bin/lib/lib64 folders are created by virutalenv.
- etc/web/logs folders are ours.

## Example template of wsgi.ini

```
[uwsgi]
socket=0.0.0.0:5501
http=0.0.0.0:5502
stats=0.0.0.0:5503
chdir=/home/your-project-name/web
processes=2
threads=40
listen=1024
master=True
daemonize=/home/your-project-name/logs/uwsgi.log
```

## Example template of wsgi.conf.py

```
bind = ["0.0.0.0:5505"]
workers = 2
threads = 40
max_requests = 10000
daemon = True
```

## Releases

### v0.3.0 2020/09/28

- Add GunicornController.

### v0.2.1 2020/09/03

- Add django-click in requriements.txt.
- Change uwsgi_ini_file search order, and uwsgi_bin search order.
- Update document.

### v0.2.0 2020/09/02

- Use as django's command.

### v0.1.3 2020/07/25

- Fix time import problem.

### v0.1.2 2020/07/25

- Fix reload parameter problem.

### v0.1.1 2020/07/25

- Fix psutil import problem.

### v0.1.0 2020/07/25

- First release.
