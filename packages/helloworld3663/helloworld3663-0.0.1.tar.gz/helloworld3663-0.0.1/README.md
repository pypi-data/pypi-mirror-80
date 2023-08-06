# Hello World

This is an example project demonstrating how to publish a python module to PyPI


## Installation

Run the following to install:

'''python
pip install helloworld3663
'''


## Usage

'''python
from helloworld3663 import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everyone"
say_hello("Everyone")
'''

# Developing Hello World

To install helloworld3663, along with the tools you need to develop and run tests, run the following in your virtualenv:

'''bash
$ pip install -e .[dev]
'''
