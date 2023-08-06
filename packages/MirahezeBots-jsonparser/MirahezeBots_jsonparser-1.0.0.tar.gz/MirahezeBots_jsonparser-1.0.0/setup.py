
from __future__ import print_function
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


setup(
    name='MirahezeBots_jsonparser',
    version='1.0.0',
    description='jsonparser utility for MirahezeBots',
    long_description=readme,
    long_description_content_type='text/markdown',  # This is important!
    author='MirahezeBot Contributors',
    author_email='bots@miraheze.org',
    url='https://github.com/MirahezeBots/jsonparser',
    packages=find_packages('.'),
    include_package_data=True,
    license='Eiffel Forum License, version 2',
)
