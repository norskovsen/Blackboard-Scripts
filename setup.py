import os
from setuptools import find_packages, setup

os.chdir(os.path.normpath(os.path.dirname(os.path.abspath(__file__))))

setup(
    name='bbdownload',
    version='0.1',
    packages=find_packages(include=['blackboard']),
    include_package_data=True,
    license='GNU GPLv3',
    description='CLI to download files from Blackboard',
    long_description='CLI to download files from BlackBoard',
    url='https://github.com/norskovsen/Blackboard-Scripts',
    author='Martin Nørskov Jensen',
    author_email='martin_n@me.com',
    install_requires=[
        'requests',
        'simplecrypt',
        'bs4',
        're',
    ],
    classifiers=[],
)
