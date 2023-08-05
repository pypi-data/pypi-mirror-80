from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['nws_alerts']

setup(
    name="nws_alerts",

    version="1.0.0",

    packages=packages,
    install_requires=[
        'nwscapparser3',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="Subscribe to alerts from the National Weather Service",
    long_description=long_description,
    license="PSF",
    keywords="grant miller national weather service nws alert common alert protocol cap",
    url="https://github.com/GrantGMiller/nws_alerts",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/nws_alerts",
    }

)
