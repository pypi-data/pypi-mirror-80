import os
from distutils.sysconfig import get_python_lib


def main():
    print('hello world')
    print('your working dir is: ', os.getcwd())
    print('python lib is: ', get_python_lib())


if __name__ == '__main__':
    main()
