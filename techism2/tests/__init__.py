import unittest

def suite():
    suite = unittest.TestSuite()
    for name in ['test_migration']:
        mod = __import__('%s.%s' % (__name__, name), {}, {}, ['suite'])
        suite.addTest(mod.suite())
    return suite
