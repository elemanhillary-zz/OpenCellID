from setuptools import setup

setup(
    name='opcipy',
    version='0.0.1',
    description='A Thin library for the OpenCellID web API products LocationIQ\
and LocationAPI',
    author="@klique",
    author_email="elemanhillary@gmail.com",
    url='http://spotipy.readthedocs.org/',
    install_requires=[
        'requests>=2.3.0',
        'six>=1.10.0',
    ],
    license='LICENSE.txt',
    packages=['opcipy'])