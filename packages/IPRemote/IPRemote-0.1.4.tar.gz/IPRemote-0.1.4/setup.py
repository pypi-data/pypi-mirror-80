#!/usr/bin/env python
import setuptools # NOQA

__title__ = "IPRemote"
__version__ = "v0.1.4"
__url__ = "https://github.com/MikishVaughn/IPRemote"
__author__ = "Michael Vaughn"
__author_email__ = "mikish.vaughn@gmail.com"
__license__ = "MIT"

setuptools.setup(
    name=__title__,
    version=__version__,
    description=__doc__,
    
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    entry_points={
        "console_scripts": ["IPRemote=IPRemote.__main__:main"]
    },
    packages=[
        "IPRemote",
        "IPRemote.upnp",
        "IPRemote.upnp.UPNP_Device",
        "IPRemote.remote_encrypted",
        "IPRemote.remote_encrypted.py3rijndael"
    ],
    install_requires=[
        'websocket-client',
        'requests',
        'lxml',
        'six',
        'ifaddr',
        'pycryptodome'
    ],
    classifiers=[        
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
    ],
    zip_safe=False
)
