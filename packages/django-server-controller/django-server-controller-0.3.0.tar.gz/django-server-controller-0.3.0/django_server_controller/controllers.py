
import os
import time

import psutil
from fastutils import fsutils
from magic_import import import_from_string

from django.conf import settings





class ControllerBase(object):

    server_bin_name = None
    config_file_name = None

    def get_default_bin(self, bin_name):
        return fsutils.first_exists_file(
            "./{0}".format(bin_name),
            "~/bin/{0}".format(bin_name),
            "~/.bin/{0}".format(bin_name),
            "./bin/{0}".format(bin_name),
            "/usr/local/bin/{0}".format(bin_name),
            "/usr/bin/{0}".format(bin_name),
            "/bin/{0}".format(bin_name),
            default="{0}".format(bin_name),
        )

    def get_default_config_file(self, config_file_name):
        if not config_file_name:
            raise RuntimeError("The controller doesn't have default config file name, so you must give config_file parameter...")
        application_init_filepath = import_from_string(settings.SETTINGS_MODULE.split(".")[0]).__file__
        application_base = os.path.dirname(application_init_filepath)
        return fsutils.first_exists_file(
            "{1}/etc/{0}".format(config_file_name, self.project_base),
            "./etc/{0}".format(config_file_name),
            "~/etc/{0}".format(config_file_name),
            "{1}/{0}".format(config_file_name, application_base),
            default=config_file_name,
        )

    def __init__(self, project_name=None, project_base=None, config_file=None, web_root=None, logs_root=None, pidfile=None, server_bin=None, **kwargs):
        self.project_name = project_name or self.get_default_project_name()
        self.project_base = project_base or self.get_default_project_base()
        os.chdir(self.project_base)
        self.config_file = config_file or self.get_default_config_file(self.config_file_name)
        self.web_root = web_root or self.get_default_web_root()
        self.logs_root = logs_root or self.get_default_logs_root()
        self.pidfile = pidfile or self.get_default_pidfile()
        self.server_bin = server_bin or self.get_default_server_bin()
        self.application = self.get_application()

    def get_default_project_base(self):
        return os.getcwd()

    def get_default_project_name(self):
        return settings.SETTINGS_MODULE.split(".")[0]

    def get_default_web_root(self):
        return os.path.abspath(os.path.join(self.project_base, "./web/"))
    
    def get_default_logs_root(self):
        return os.path.abspath(os.path.join(self.project_base, "./logs/"))

    def get_default_pidfile(self):
        return os.path.abspath(os.path.join(self.project_base, "./{}.pid".format(self.project_name)))

    def get_application(self):
        return settings.SETTINGS_MODULE.split(".")[0] + ".wsgi:application"

    def get_default_server_bin(self):
        if not self.server_bin_name:
            raise NotImplementedError()

        return self.get_default_bin(self.server_bin_name)

    def get_server_pid(self):
        if not os.path.isfile(self.pidfile):
            return 0
        with open(self.pidfile, "r", encoding="utf-8") as fobj:
            return int(fobj.read().strip())

    def get_running_server_pid(self):
        pid = self.get_server_pid()
        if not pid:
            return 0
        if psutil.pid_exists(pid):
            return pid
        else:
            return 0

    def get_start_command(self):
        raise NotImplementedError()

    def get_stop_command(self):
        raise NotImplementedError()
    
    def get_reload_command(self):
        raise NotImplementedError()

    def start(self):
        """Start server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            pid = self.get_server_pid()
            print("service is running: {}...".format(pid))
            os.sys.exit(1)
        else:
            print("Start server...")
            cmd = self.get_start_command()
            print("command:", cmd)
            os.system(cmd)
            print("server started!")

    def stop(self):
        """Stop server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("Stop server...")
            cmd = self.get_stop_command()
            print(cmd)
            os.system(cmd)
            print("server stopped!")
        else:
            print("service is NOT running!")

    def reload(self):
        """Reload server.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("Reload server...")
            cmd = self.get_reload_command()
            print(cmd)
            os.system(cmd)
            print("server reloaded!")
        else:
            print("service is NOT running, try to start it!")
            self.start()

    def restart(self, wait_seconds=2):
        """Restart server.
        """
        self.stop()
        if wait_seconds:
            time.sleep(wait_seconds)
        self.start()

    def status(self):
        """Get server status.
        """
        os.chdir(self.web_root)
        pid = self.get_running_server_pid()
        if pid:
            print("server is running: {0}.".format(pid))
        else:
            print("server is NOT running.")
 
    def make_controller(self, main, click_lib):

        @main.command()
        def reload():
            """Reload server.
            """
            self.reload()

        @main.command()
        @click_lib.option("-w", "--wait-seconds", type=int, default=2, help="Wait some seconds after stop and before start the server.")
        def restart(wait_seconds):
            """Restart server.
            """
            self.restart(wait_seconds)

        @main.command()
        def start():
            """Start server.
            """
            self.start()

        @main.command()
        def stop():
            """Stop server.
            """
            self.stop()

        @main.command()
        def status():
            """Get server's status.
            """
            self.status()

        return main

class UwsgiController(ControllerBase):

    server_bin_name = "uwsgi"
    config_file_name = "wsgi.ini"

    def get_start_command(self):
        return "{server_bin} {config_file} --pidfile={pidfile} --wsgi={application}".format(
            server_bin=self.server_bin,
            config_file=self.config_file,
            pidfile=self.pidfile,
            application=self.application,
            )

    def get_stop_command(self):
        return "{server_bin} --stop {pidfile}".format(
            server_bin=self.server_bin,
            pidfile=self.pidfile,
            )
    
    def get_reload_command(self):
        return "{server_bin} --reload {pidfile}".format(
            server_bin=self.server_bin,
            pidfile=self.pidfile,
            )


class GunicornController(ControllerBase):
    
    server_bin_name = "gunicorn"
    config_file_name = "wsgi.conf.py"

    def get_default_kill_bin(self):
        return self.get_default_bin("kill")

    def __init__(self, kill_bin=None, **kwargs):
        super().__init__(**kwargs)
        self.kill_bin = kill_bin or self.get_default_kill_bin()

    def get_start_command(self):
        return "{server_bin} --config={config_file} --pid={pidfile} {application}".format(
            server_bin=self.server_bin,
            config_file=self.config_file,
            pidfile=self.pidfile,
            application=self.application,
        )

    def get_stop_command(self):
        pid = self.get_running_server_pid()
        if pid:
            return "{kill_bin} -TERM {pid}".format(kill_bin=self.kill_bin, pid=pid)
        else:
            return "echo NOT RUNNING..."

    def get_reload_command(self):
        pid = self.get_running_server_pid()
        if pid:
            return "{kill_bin} -HUP {pid}".format(kill_bin=self.kill_bin, pid=pid)
        else:
            return "echo NOT RUNNING..."
