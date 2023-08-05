from setuptools import setup

setup(
    name='domination',
    author='Baptiste Azéma',
    author_email='baptiste@azema.tech',
    version='1.0',
    packages=['domination'],
    include_package_data=True,
    python_requires='~=3.6',
    description='Real-time application in order to dominate Humans.',
    license='LICENSE',
    entry_points={
        'console_scripts': ['domination=domination.__main__:main']
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
