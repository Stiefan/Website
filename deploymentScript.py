# -*- coding: utf-8 -*-
#!/user/bin/env python2.7

from deployer.client import start
from deployer.node import Node

from deployer.utils import esc1
from deployer.host import SSHHost

django_settings = \
    """
    DATABASES['default'] = ...
    SESSION_ENGINE = ...
    DEFAULT_FILE_STORAGE = ...
    """
supervisor_config = \
"""
[program:djangoproject]
command = /home/username/.virtualenvs/project-env/bin/gunicorn_start  ; Command to start app
user = username                                                       ; User to run as
stdout_logfile = /home/username/logs/gunicorn_supervisor.log          ; Where to write log messages
redirect_stderr = true                                                ; Save stderr in the same log
"""

class remote_host(SSHHost):
    address = 'web0104.zxcs.nl:7685'
    username = 'u11275d26494'
    password = 'BPjnaxbc'
    key_filename = None

class DjangoDeployment(Node):

    class Hosts:
        host = remote_host

    project_directory = '~/git/django-project'
    repository = 'git@github.com:Stiefan/Website.git'

    def install_git(self):
        """ Installs the ``git`` package. """
        self.host.sudo('apt-get install git')

    def git_clone(self):
        """ Clone repository."""
        with self.host.cd(self.project_directory, expand=True):
            self.host.run("git clone '%s'" % esc1(self.repository))

    def git_checkout(self, commit):
        """ Checkout specific commit (after cloning)."""
        with self.host.cd(self.project_directory, expand=True):
            self.host.run("git checkout '%s'" % esc1(commit))

    def upload_django_settings(self):
        """ Upload the content of the variable 'local_settings' in the
        local_settings.py file. """
        with self.host.open('~/git/django-project/local_settings.py') as f:
            f.write(django_settings)

    activate_cmd = '. ~/.virtualenvs/project-env/bin/activate'

    def install_requirements(self):
        """
        Script to install the requirements of our Django application.
        (We have a requirements.txt file in our repository.)
        """
        with self.host.prefix(self.activate_cmd):
            self.host.run('pip install -r ~/git/django-project/requirements.txt')

    def install_package(self, name):
        """
        Utility for installing packages through ``pip install`` inside
        the env.
        """
        with self.host.prefix(self.activate_cmd):
            self.host.run('pip install %s' %name)

    def run_management_command(self, command):
        """ Run Django management command in virtualenv. """
        # Activate the virtualenv.
        with self.host.prefix(self.activate_cmd):
            # Go to the directory where we have our 'manage.py' file.
            with self.host.cd('~/git/django-project/'):
                self.host.run('./manage.py %s' % command)

    def django_shell(self):
        """ Open interactive Django shell. """
        self.run_management_command('shell')

    def install_gunicorn(self):
        """ Install gunicorn inside the virtualenv. """
        self.install_package('gunicorn')

    def install_supervisord(self):
        """ Install supervisord inside the virtualenv. """
        self.install_package('supervisor')

    def run_gunicorn(self):
        """ Run the gunicorn server """
        self.run_management_command('run_gunicorn')

    def upload_supervisor_config(self):
        """ Upload the content of the variable 'supervisor_config' in the
        supervisord configuration file. """
        with self.host.open('/etc/supervisor/conf.d/django-project.conf') as f:
            f.write(supervisor_config)

if __name__ == '__main__':
    start(DjangoDeployment)