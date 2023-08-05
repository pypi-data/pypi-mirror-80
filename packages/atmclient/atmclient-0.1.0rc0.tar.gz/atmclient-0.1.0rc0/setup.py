import os
import setuptools

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


long_description = """
ATM v2 API Protocol Compliant Client
    
This script is designed to communicate with 
the ATM Code Standard(Chan Woo Kim, Jung Jung Ho) compliant ATM v2 API
Developers can use this module to conveniently utilize the various engines 
and shared functions in the LXPER Kubernetes on-premises environment.
It has no dependencies other than the Python Standard Library.
"""

setuptools.setup(
    name="atmclient", # Replace with your own username
    version=get_version("atmclient/__init__.py"),
    author="LXPER",
    author_email="lxpermanager@naver.com",
    description="ATM v2 API Protocol Compliant Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.lxper.com",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)