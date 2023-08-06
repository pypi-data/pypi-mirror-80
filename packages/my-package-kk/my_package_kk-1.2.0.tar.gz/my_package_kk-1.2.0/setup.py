from setuptools import find_packages, setup

setup(
    name='my_package_kk',
    version='1.2.0',
    author='kk12pt',
    author_email='spam@12pt.pl',
    packages=find_packages(),
    include_package_data=True,
    description='hi fi super star',
    install_requires = ['names'],
    scripts= ['bin/get_name_kkubiak.py', 'bin/get_name_kkubiak.bat']
)
