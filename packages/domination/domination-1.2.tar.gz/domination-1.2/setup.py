from pkg_resources import parse_requirements
from setuptools import setup

REQUIREMENTS = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='domination',
    author='Baptiste Azéma',
    author_email='baptiste@azema.tech',
    version='1.2',
    packages=['domination'],
    include_package_data=True,
    python_requires='~=3.6',
    install_requires=REQUIREMENTS,
    description='Real-time application in order to dominate Humans.',
    license='LICENSE',
    entry_points={
        'console_scripts': ['domination=domination.__main__:main']
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
