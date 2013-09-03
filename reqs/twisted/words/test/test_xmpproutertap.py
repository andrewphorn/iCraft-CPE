# Copyright (c) 2001-2008 Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{twisted.words.xmpproutertap}.
"""

from reqs.twisted.application import internet
from reqs.twisted.trial import unittest
from reqs.twisted.words import xmpproutertap as tap
from reqs.twisted.words.protocols.jabber import component

class XMPPRouterTapTest(unittest.TestCase):

    def test_port(self):
        """
        The port option is recognised as a parameter.
        """
        opt = tap.Options()
        opt.parseOptions(['--port', '7001'])
        self.assertEquals(opt['port'], '7001')


    def test_portDefault(self):
        """
        The port option has '5347' as default value
        """
        opt = tap.Options()
        opt.parseOptions([])
        self.assertEquals(opt['port'], 'tcp:5347:interface=127.0.0.1')


    def test_secret(self):
        """
        The secret option is recognised as a parameter.
        """
        opt = tap.Options()
        opt.parseOptions(['--secret', 'hushhush'])
        self.assertEquals(opt['secret'], 'hushhush')


    def test_secretDefault(self):
        """
        The secret option has 'secret' as default value
        """
        opt = tap.Options()
        opt.parseOptions([])
        self.assertEquals(opt['secret'], 'secret')


    def test_verbose(self):
        """
        The verbose option is recognised as a flag.
        """
        opt = tap.Options()
        opt.parseOptions(['--verbose'])
        self.assertTrue(opt['verbose'])


    def test_makeService(self):
        """
        The service gets set up with a router and factory.
        """
        opt = tap.Options()
        opt.parseOptions([])
        s = tap.makeService(opt)
        self.assertIsInstance(s, internet.TCPServer)
        self.assertEquals('127.0.0.1', s.kwargs['interface'])
        self.assertEquals(2, len(s.args))
        self.assertEquals(5347, s.args[0])
        factory = s.args[1]
        self.assertIsInstance(factory, component.XMPPComponentServerFactory)
        self.assertIsInstance(factory.router, component.Router)
        self.assertEquals('secret', factory.secret)
        self.assertFalse(factory.logTraffic)


    def test_makeServiceVerbose(self):
        """
        The verbose flag enables traffic logging.
        """
        opt = tap.Options()
        opt.parseOptions(['--verbose'])
        s = tap.makeService(opt)
        factory = s.args[1]
        self.assertTrue(factory.logTraffic)
