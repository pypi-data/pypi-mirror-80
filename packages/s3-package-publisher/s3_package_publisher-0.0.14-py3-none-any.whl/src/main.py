import os
from distutils.sysconfig import get_python_lib


def main():
    print('get_python_lib(): ', get_python_lib())
    print('os.path.dirname(__file__): ', os.path.dirname(__file__))


if __name__ == '__main__':
    main()
