import subprocess
from typing import TypeVar
import os
import sys

Command = TypeVar('Command', bound=str)


def __run_command(command: Command) -> int:
    return subprocess.run([x.strip() for x in command.split() if x != '']).returncode


def main():
    print('sys.argv', sys.argv)
    distribute: Command = '''
    pipenv run pipenv-setup sync &
    AWS_ACCESS_KEY_ID="%s"
    AWS_SECRET_ACCESS_KEY="%s"
    AWS_DEFAULT_REGION="us-east-1"
    pipenv run s3pypi --bucket "%s" --verbose
    ''' % (os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'), sys.argv[1])

    bump_version: Command = '''
    git reset --hard HEAD &
    git config --global user.email "bumpversion@circleci.com" &
    git config --global user.name "bumpversion" &
    echo "Bumping version" &
    pipenv run bumpversion
    --current-version "$(pipenv run python setup.py --version)"
    --verbose --commit --tag
    --message "Bump version: {current_version} → {new_version} [skip ci]"
    patch setup.py &
    echo "Pushing" &
    git push
    '''

    if __run_command(distribute) != 0:
        __run_command(bump_version)
        __run_command(distribute)


if __name__ == '__main__':
    main()
