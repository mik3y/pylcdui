#!/usr/bin/env/python

from distutils.core import setup

setup(
    name = "pylcdui",
    version = "0.5.4",
    description = "Library for CrystalFontz and Matrix-Orbital LCD displays",
    author = "mike wakerly",
    author_email = "opensource@hoho.com",
    url = "http://code.google.com/p/pylcdui/",
    packages = [
      'lcdui',
      'lcdui.core',
      'lcdui.ui',
      'lcdui.devices',
    ],
)
