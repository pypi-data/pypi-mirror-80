# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import unittest


################################################
##################### Main #####################
def tests()->bool:
    tests = unittest.TestLoader().discover("tfsm/tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful(): return 0
    else: return 1

if __name__ == "__main__":
    tests()