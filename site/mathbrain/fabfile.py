import socket
import os
import pwd
import getpass
import datetime

from fabric.api import *
from fabric.contrib import *
from fabric.context_managers import *
from fabric.utils import *

from fabric.contrib.files import sed


def localhost():
    env.hosts = ['localhost']


def production():
    env.hosts = ['newton.mathbrain.com.au']
    env.deploy_user = 'mathbrain'
    env.approot = 'mathbrain'
    env.coderoot = 'mathbrain/site/mathbrain'


def start():
    localhost()
    local('git pull')
    local('python manage.py runserver', capture=False)


def archive():
    run('git archive HEAD --format=zip > /tmp/mathbrain.zip')


def virtualenv(command):
    run(env.activate + ' && ' + command)


@hosts('mathbrain@newton.mathbrain.com.au')
def deploy():
    production()

    today = str(datetime.date.today())

    with cd(env.approot):
        run('git checkout -- site/mathbrain/mathbrain/settings.py')
        run('git pull')

    with cd(env.coderoot):
        with settings(warn_only=True):
            run('kill -9 `cat /tmp/django.pid`')
            run('rm /tmp/django.pid')
        run('python manage.py dumpdata registration --indent=2 > ' \
            '/tmp/mathbrain-registration-dbdump-%s.json' % today)
        run('python manage.py syncdb')
        run('python manage.py collectstatic --noinput')
        sed('/home/mathbrain/mathbrain/site/mathbrain/mathbrain/settings.py', 
                '^DEBUG = True$',
                'DEBUG = False') 
        run('python manage.py loaddata ' \
            '/tmp/mathbrain-registration-dbdump-%s.json' % today)
        run('python manage.py runfcgi method=threaded host=127.0.0.1' \
                ' port=8000 pidfile=/tmp/django.pid' \
                ' outlog=/var/log/mathbrain/access.log' \
                ' errlog=/var/log/mathbrain/error.log')

