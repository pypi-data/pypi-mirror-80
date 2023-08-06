# -*- mode: python; coding: utf-8 -*-
# Copyright 2020 Peter Williams
# Licensed under the MIT License

from setuptools import setup, Extension

setup_args = dict(
    name = 'cranko',
    version = '0.1.0',
    description = 'Placeholder for the Cranko release automation tool',
    long_description = '''
This is a placeholder package created to entitle the "Cranko"
release automation tool to use the `tool.cranko` namespace in
`pyproject.toml` files, as per PEP 518.''',
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/pkgw/cranko',
    license = 'MIT',
    author = 'Peter Williams',
    author_email = 'peter@newton.cx',
    packages = ['cranko'],
)

if __name__ == '__main__':
    setup(**setup_args)
