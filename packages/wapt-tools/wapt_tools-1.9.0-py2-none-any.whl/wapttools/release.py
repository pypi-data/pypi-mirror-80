import datetime
import logging
import os
import subprocess
from .config import loadControl

log = logging.getLogger()


def release():
    """ Release a package
    """
    version = loadControl()['version']
    hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
    date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    branch = 'release/v{version}-{hash}'.format(version=version, hash=hash)
    message = '"Release v{version} ({hash}) on {date}"'.format(version=version, hash=hash, date=date)
    message_noci = message[:-1] + ' [skip ci]"'

    command = 'git checkout -b {branch} develop'.format(branch=branch)
    log.debug(command)
    os.system(command)

    command = 'git checkout master'
    log.debug(command)
    os.system(command)

    command = 'git merge --no-ff {branch} --no-commit'.format(branch=branch)
    log.debug(command)
    os.system(command)

    command = 'git commit -m {message}'.format(message=message)
    log.debug(command)
    os.system(command)

    command = 'git tag -a v{version}-{hash} -m {message}'.format(version=version, hash=hash, message=message)
    log.debug(command)
    os.system(command)

    command = 'git checkout develop'
    log.debug(command)
    os.system(command)

    command = 'git merge --no-ff {branch} --no-commit'.format(branch=branch)
    log.debug(command)
    os.system(command)

    command = 'git commit -m {message}'.format(message=message_noci)
    log.debug(command)
    os.system(command)

    command = 'git branch -d {branch}'.format(branch=branch)
    log.debug(command)
    os.system(command)

    command = 'git push --all'
    log.debug(command)
    os.system(command)

    command = 'git push --tags'
    log.debug(command)
    os.system(command)
