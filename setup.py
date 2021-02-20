#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as changelog_file:
    changelog = changelog_file.read()

with open('VERSION') as version_file:
    version = version_file.read().replace('\n', '')

with open('requirements.txt') as requirements_file:
    # The requirements need to be a list of strings. That is why we are using readline here instead of read
    requirements = readme_file.readlines()
    # The requirements file still contains some empty lines and comments, which need to be cleaned up
    requirements = [line for line in requirements if line != '' and not line.startswith('#')]
    requirements = ['click==7.1.2']


setup(
    author='Jonas Teufel',
    author_email='jonseb1998@gmail.com',
    python_requires='>=3.6',
    description='A python web application to track scientific publicatio status within the KITOpen database',
    entry_points={
        'console_scripts': [
            'pubtrack=pubtrack.cli:cli'
        ]
    },
    install_requirements=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + changelog,
    include_package_data=True,
    keywords='pubtrack',
    name='pubtrack',
    packages=find_packages(include=['pubtrack', 'pubtrack.*']),
    url='https://github.com/the16thpythonist/pubtrack',
    version=version,
    zip_safe=False
)