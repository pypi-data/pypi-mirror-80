#!/usr/bin/env python

import setuptools
import src.codetags as package

setuptools.setup(
  name = 'codetags',
  version = package.__version__,
  description = package.__doc__.strip(),
  author = package.__author__,
  author_email = package.__author_email__,
  license = package.__license__,
  url = 'https://github.com/molurusio/codetags',
  download_url = 'https://github.com/molurusio/codetags/downloads',
  keywords = ['molurus', 'feature-toggle'],
  classifiers = [],
  install_requires = open("requirements.txt").readlines(),
  package_dir = {'':'src'},
  packages = setuptools.find_packages('src'),
)