import os
import requests
import json

from django.conf import settings

from fabric.api import env, sudo as _sudo, run as _run
from fabric.operations import *
from fabric.contrib import files as f
from fabric.colors import red, green, blue


"""
What the fab script does:
The script is meant to deploy a bookshop application to a digital ocean vsp (works with any vps). Server configurations are found in
a deploy folder within the project root. Virtualenv is inside the project root as well.
1. Prepare fresh environment - Install sudo apt-packages (nginx, php, python, python-pip)
2. Create directory
3. Clone repository
4. Create virtualenvironment
5. Install Requirements
6. Run using gunicorn, supervisor, and nginx

Upon deployment, hit fab prod deploy

Enjoy!

"""

""" DB CONFIGURATION """
db_name = ""
db_user = ""
db_pass = ""

deployer = input("Please write your name: ")
repo_url = "https://gitlab.com/finx-ms/finx-account.git"


def staging():
    send_message_to_slack(
        "> *{}* is now aiming FINX ACCOUNT STAGING server \
        :bow_and_arrow:".format(
            deployer
        )
    )

    env.hosts = [
        "172.104.60.212",
    ]
    env.user = "sagara"
    env.password = "barakadut1234"
    env.folder = "staging"

    env.use_ssh_config = False
    env.port = 22
    env.timeout = 20
    env.purpose = f"finx.id"
    env.service = "account.finx.id"

    env.project = f"/opt/app/{env.purpose}/"
    env.project_env = "{}venv/".format(env.project)
    env.project_root = "{}account.finx.id/".format(env.project)
    env.local_settings = os.path.join(os.getcwd(), "staging/local_settings.py")
    env.systemd = "{}deploy/{}/{}.service".format(
        env.project_root, env.folder, env.service
    )
    env.name = "development"


def turn_off_all():
    print(red("[Turning Supervisor OFF]"))
    _sudo("systemctl stop {}.service".format(env.service))


def turn_on_all():
    print(green("[Turning Supervisor ON]"))
    _sudo("systemctl start {}.service".format(env.service))


def restart_service():
    print(green("[Restarting Supervisor]"))
    _sudo("systemctl restart {}.service".format(env.service))


def preparing_dir():
    if not f.exists(env.project):
        print(green("Creating project directory..."))
        if not f.exists("/opt/app/"):
            _sudo("cd /opt/ && mkdir app")

        _sudo(
            "cd /opt/app/ && mkdir {} \
               && chown -R {}:{} /opt".format(
                env.purpose, env.user, env.user
            )
        )


def checking_virtualenv():
    # cleanup current env
    print(green("[CHECKING VIRTUAL ENVIRONMENT]"))
    if not f.exists(env.project_env):
        print(green("[CREATE FRESH ENVIRONMENT]"))
        _run("cd {} && virtualenv -p python3 venv".format(env.project))


def preparing_virtualenv():
    # cleanup current env
    print(green("[PREPARING VIRTUAL ENVIRONMENT]"))
    if f.exists(env.project_env):
        print(red("[REMOVE VIRTUAL ENVIRONMENT]"))
        _run("cd {} && rm -rf venv".format(env.project))

    # create fresh env
    print(green("[CREATE FRESH ENVIRONMENT]"))
    _run("cd {} && virtualenv -p python3 venv".format(env.project))


def install_requirements():
    print(blue("[Upgrading pip and setuptools Requirements...]"))
    _run(
        "cd {} && source ../venv/bin/activate && pip install pip --upgrade \
          && pip install setuptools --upgrade".format(
            env.project_root
        )
    )
    print(blue("[Installing Requirements...]"))
    _run(
        "cd {} && source ../venv/bin/activate \
          && export CPLUS_INCLUDE_PATH=/usr/include/gdal \
          && export C_INCLUDE_PATH=/usr/include/gdal \
          && pip install -r requirements.dev.txt".format(
            env.project_root
        )
    )


def pull_code():
    print(green("[PULLING CODE]"))
    _run(
        "source {}bin/activate && cd {} \
          && git pull origin {}".format(
            env.project_env, env.project_root, env.name
        )
    )


def clone_repo():
    print(red("[Cloning repository ...]"))
    _run(
        "source {}bin/activate && cd {} \
          && git clone -b {} {} account.finx.id".format(
            env.project_env, env.project, env.name, repo_url
        )
    )


def support_directory():
    # create support directories
    print(blue("[Creating support directories]"))
    if not f.exists("{}run".format(env.project)):
        _run("cd {} && mkdir run".format(env.project))
    if not f.exists("{}logs".format(env.project)):
        _run("cd {} &&  mkdir logs".format(env.project))


def copy_local_settings():
    print(red("Copying local settings..."))
    if f.exists(env.project_root + "project/local_settings.py"):
        _run("rm {}project/local_settings.py ".format(env.project_root))

    put(env.local_settings, "{}project/local_settings.py".format(env.project_root))


def create_systemd_file():
    print(red("Creating systemd file..."))
    _sudo("cp {} /etc/systemd/system/".format(env.systemd))


def remove_migrations():
    print(red("Removing migrations directory ..."))
    _sudo(
        "source {}bin/activate && cd {}src/enterprise/enterprise/ \
                   && rm -rf structures/**/migrations/".format(
            env.project_env, env.project_env
        )
    )


def send_message_to_slack(
    message, channel="proj-investx", username="fabric", emoji=":satellite_antenna:"
):
    pass
    """
    url = 'https://hooks.slack.com/services/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'
    payload = {
        'channel': '#%s' % channel,
        'username': username,
        'text': message,
        'icon_emoji': emoji
    }
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    requests.post(url, data=json.dumps(payload), headers=headers)
    """


def set_owner():
    _sudo("chown -R {}:{} /opt/app ".format(env.user, env.user))


def reload_systemd():
    _sudo("systemctl daemon-reload")


def deploy():
    send_message_to_slack(
        "> *" + deployer + "* is now attempting to deploy :hammer_and_pick:"
    )
    if f.exists(env.project_root):
        pull_code()
    else:
        fresh_deploy()

    create_systemd_file()
    install_requirements()
    # remove_migrations()
    copy_local_settings()
    reload_systemd()
    # restart_service()
    turn_off_all()
    turn_on_all()
    send_message_to_slack("> Deployment success :thumbsup_all:")


def fresh_deploy():
    # create directory
    preparing_dir()

    # change owner
    set_owner()

    # check virtual env
    checking_virtualenv()

    # clone repository
    clone_repo()

    support_directory()


def restart():
    send_message_to_slack(
        "> *" + deployer + "* is now attempting to restart :electric_plug:"
    )
    turn_off_all()
    turn_on_all()
    send_message_to_slack("> System restarted :thumbsup_all:")
