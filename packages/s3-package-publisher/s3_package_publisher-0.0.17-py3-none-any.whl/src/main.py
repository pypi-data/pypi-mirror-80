import subprocess
import sys
from typing import List
import os


def __run_command(argstr: str) -> int:
    return subprocess.run(argstr.strip().split()).returncode


def __distribute(bucket: str) -> int:
    __run_command('pipenv run pipenv-setup sync')
    return __run_command('pipenv run s3pypi --bucket %s --verbose' % bucket)


def __bump_version():
    __run_command('git checkout HEAD -- setup.py')
    __run_command('git config --global user.email "bumpversion@circleci.com"')
    __run_command('git config --global user.name "bumpversion"')
    current_version = subprocess.check_output('pipenv run python setup.py --version'.split())
    print('current_version: ', current_version)
    __run_command('''
        pipenv run bumpversion
        --current-version %s --verbose --commit --tag
        --message "Bump version: {current_version} → {new_version} [skip ci]"
        patch setup.py
    ''' % current_version)
    __run_command('git push')


def main():
    missing_env_vars: List[str] = []
    required_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY']
    for required_env_var in required_env_vars:
        if not os.environ.get(required_env_var):
            missing_env_vars.append(required_env_var)
    if missing_env_vars:
        print("Missing required environment variable(s): ", ', '.join(missing_env_vars))
        exit(1)
    bucket = sys.argv[1]
    if __distribute(bucket) != 0:
        __bump_version()
        __distribute(bucket)


if __name__ == '__main__':
    main()
