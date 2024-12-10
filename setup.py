#!/usr/bin/python3

from setuptools import setup
import os

# Load __version__ from cmdqueue/version.py
exec(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cmdqueue/version.py")).read())

setup(
    name='cmdqueue',
    version=__version__,
    description='Queue shell commands',
    author='Dominik Heidler',
    author_email='dheidler@suse.de',
    install_requires=['termcolor', 'tomlkit'],
    packages=['cmdqueue'],
    scripts=['bin/queue'],
)
