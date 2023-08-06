# encoding: utf-8
#!/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
	name = "BioCircos",
	version = "0.0.1",
	author = "Junhao Deng",
	author_email = "1135520789@qq.com",
	description = "BioCircos plot",
	long_description = open("README.rst").read(),
	license = "MIT",
	url="https://github.com/djh1991/BioCircos",
	packages = ["BioCircos"],
	install_requires = ['reportlab'],
	classifiers = [
		"Environment :: Web Environment",
		"Intended Audience :: Developers",
		"Operating System :: OS Independent",
		"Topic :: Text Processing :: Indexing",
		"Topic :: Utilities",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.6",
		"Programming Language :: Python :: 2.7",
	],
	
)