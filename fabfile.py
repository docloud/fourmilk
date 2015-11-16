# coding=utf8

from fabric.api import (
    run,
    put,
    task,
    env,
    cd
)
from fabric.contrib.project import rsync_project


@task
def deploy(host):
    env.user = "runner"
    env.host_string = host
    env.use_ssh_config = True

    rsync_project(local_dir=".", remote_dir="/srv/fourmilk", exclude=(".git", ".idea"))
    with cd("/srv/fourmilk"):
        run("sudo make develop")
        run("sudo supervisorctl restart fourmilk")
