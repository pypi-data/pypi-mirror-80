# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import unittest

from tfsm import fsm, settings
from tfsm.models import *


################################################
################### Test(s) ####################

class TestModels(unittest.TestCase):

    def test_models(self):
        tco = TfsmInput("AAPL", settings.TIME_ZONE)

        for _ in range(50000):
            tco.get()
            tco.tick()

        tco.show()
        self.assertEqual(tco.metrics.size(), settings.SIZE_OF_DATA)
        
        tco.call("alpha", Intent.LONG)
        self.assertEqual(len(tco.active_claims()), 1)
        
        tco.get()
        tco.tick()

        tco.call("beta", Intent.SHORT)
        self.assertEqual(tco.active_claims()[0].intent, Intent.SHORT)
        
        tco.get()
        tco.tick()

        tco.call("charlie", Intent.LONG)
        tco.cover("alpha")
        self.assertEqual(len(tco.active_claims()), 2)
    
if __name__ == "__main__":
    unittest.main()
