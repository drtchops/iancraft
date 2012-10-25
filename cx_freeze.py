from cx_Freeze import setup
from cx_Freeze import Executable
import sys
import os

parent_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path[0] = parent_path

setup(
    name='iancraft',
    version='0.12',
    description='The greatest RTS known to man.',
    url='http://elvenrealms.net:8080/psts',
    author='Ian Robinson',
    author_email='ian_robinson@rogers.com',
    license='Copyright (c) 2012 Ian Robinson.',
    data_files=['graphics', 'sound', 'scenarios', 'default.ini',
            'readme.txt', 'changelog.txt'],
    executables=[Executable('main.py', packages=['iancraft'])])
