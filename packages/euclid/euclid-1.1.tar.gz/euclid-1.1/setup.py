#!/usr/bin/env python

'''
'''

from distutils.core import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='euclid',
      version='1.1',
      description='2D and 3D vector, matrix, quaternion and geometry module',
      author='Alex Holkner',
      author_email='alex@partiallydisassembled.net',
      maintainer='Richard Jones',
      maintainer_email='r1chardj0n3s@gmail.com',
      url='https://github.com/r1chardj0n3s/euclid',
      py_modules=['euclid'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      )

