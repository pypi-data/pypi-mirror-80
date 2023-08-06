# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
from tfsm import fsm


################################################
################## Export(s) ###################
null = fsm.State("Null")
start = fsm.State("Start")
end = fsm.State("End")

connect = fsm.State("Connect")
market = fsm.State("Market")
tick = fsm.State("Tick")
algorithm = fsm.State("Algorithm")
