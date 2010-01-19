#!/usr/bin/env/python

from distutils.core import setup

setup(
    name = "pylcdui",
    version = "0.5.0",
    description = "Python character LCD library",
    author = "mike wakerly",
    author_email = "opensource@hoho.com",
    url = "http://code.google.com/p/pylcdui/",
    packages = [
      'lcdui',
      'lcdui.core',
      'lcdui.devices',
    ],
    package_dir = {
      'lcdui': '',
    },
)
