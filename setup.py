#!/usr/bin/env python

from distutils.core import setup

__version__ = '0.0.0.1'
__author__ = 'r-p1e'


def project_description():
    return """
           gripari-ftp is one of the griapries which will load
           data from ftp server.
           """

setup(name="gripari-ftp",
      version=__version__,
      description=project_description(),
      author=__author__,
      author_email="r-p1e@protonmail.com",
      url="https://www.github.com/r-p1e/gripari-ftp",
      packages=["gripari-ftp"],
      package_dir={"gripari-ftp": "src"},
      )
