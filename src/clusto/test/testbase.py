import sys
import os

sys.path.insert(0, os.curdir)


import unittest

import clusto

DB='sqlite:///:memory:'
ECHO=False

class ClustoTestResult(unittest.TestResult):
    def addError(self, test, err):
        """Called when an error has occurred. 'err' is a tuple of values as
        returned by sys.exc_info().
        """
        print >>sys.stderr, "ERROR HERE!"
        clusto.rollback_transaction()
        self.errors.append((test, self._exc_info_to_string(err, test)))
        


class ClustoTestBase(unittest.TestCase):



    def data(self):
        pass
    
    def setUp(self):

        clusto.connect(DB,echo=ECHO)
        clusto.init_clusto()
        self.data()


    def tearDown(self):

        clusto.clear()
        clusto.disconnect()
        clusto.METADATA.drop_all()



    def defaultTestResult(self):
        if not hasattr(self._testresult):
            self._testresult = ClustoTestResult()

        return self._testresult

