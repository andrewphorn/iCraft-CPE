
# Copyright (c) 2001-2004 Twisted Matrix Laboratories.
# See LICENSE for details.


"""
Support module for making TOC servers with twistd.
"""

from reqs.twisted.words.protocols import toc
from reqs.twisted.python import usage
from reqs.twisted.application import strports

class Options(usage.Options):
    synopsis = "[-p <port>]"
    optParameters = [["port", "p", "5190"]]
    longdesc = "Makes a TOC server."

def makeService(config):
    return strports.service(config['port'], toc.TOCFactory())
