#!/usr/bin/env python

import os, sys

def registerRelativePath(myself, *relative_paths):
  sys.path.append(os.path.join(os.path.dirname(os.path.realpath(myself)), *relative_paths))
