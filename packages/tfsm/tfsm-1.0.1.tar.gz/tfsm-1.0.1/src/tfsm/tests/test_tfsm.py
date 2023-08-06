# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import unittest

from tfsm import fsm, machines, settings
from tfsm.models import *


################################################
################### Test(s) ####################
class TestTfsm(unittest.TestCase):

    def test_talg(self):
        tco = TfsmInput("AAPL", settings.TIME_ZONE)
        tco.show()

        fsm_talg = machines.build_talg()

        counter = 0
        while counter < 110000: 
            tco.get()
            tco.tick()
            fsm_talg.run(tco)

            counter += 1
        tco.show()

    def test_tfsm(self):
        tco = TfsmInput("AAPL", settings.TIME_ZONE)

        fsm_tsys = machines.build_tsys()
        fsm_talg = machines.build_talg()
        
        counter = 0
        state = fsm_tsys.initial_state
        while counter < 300: 
            if state == machines.tsys.S.algorithm: 
                fsm_talg.run(tco)
                tco.show()
            
            state, tco = fsm_tsys.next_state(state, tco)
            counter += 1

if __name__ == "__main__":
    unittest.main()
