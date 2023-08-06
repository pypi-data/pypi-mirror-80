import subprocess
from typing import TypeVar, List
import sys

from pipenv_setup.__main__ import cmd as pipenv_setup
from s3pypi.__main__ import main as s3pypi
from bumpversion.__main__ import main as bumpversion

Command = TypeVar('Command', bound=str)


def __run_command(command: Command) -> int:
    return subprocess.run([x.strip() for x in command.split() if x != '']).returncode


def __to_args(argstr: str) -> List[str]:
    return ['foobar.py'] + argstr.strip().split()


def __distribute(bucket: str):
    pipenv_setup(__to_args('sync'))
    s3pypi(__to_args('--bucket %s --verbose' % bucket))


def __bump_version():
    subprocess.run('git reset --hard HEAD'.split())
    subprocess.run('git config --global user.email "bumpversion@circleci.com"'.split())
    subprocess.run('git config --global user.name "bumpversion"'.split())
    current_version = subprocess.check_output('pipenv run python setup.py --version'.split())
    bumpversion(__to_args('''
        --current-version %s --verbose --commit --tag
        --message "Bump version: {current_version} → {new_version} [skip ci]"
        patch setup.py
    ''' % current_version))
    subprocess.run('git push'.split())


def main():
    try:
        __distribute(sys.argv[1])
    except:
        __bump_version()
        __distribute(sys.argv[1])


if __name__ == '__main__':
    main()
