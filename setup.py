#!/usr/bin/env python

from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "pylcdui",
    version = "0.5.7",
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
