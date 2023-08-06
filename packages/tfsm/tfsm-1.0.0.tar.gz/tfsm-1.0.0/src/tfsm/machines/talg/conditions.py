# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
from tfsm import exceptions, fsm, models, settings, utils as u
from tfsm.machines.talg import parameters as p


################################################
################# Condition(s) #################
class IsReady(fsm.Condition):
    def yes(self, i):
        case = i.ready
        if settings.DEBUG: i.log.debug(f"TALG - condition=is_ready: case={case}")
        return case

class CallAlpha(fsm.Condition):
    def yes(self, i):
        case = not i.claim(p.ALPHA_ALIAS) and i.datetime() < u.today(p.ALPHA_TIME_ENTER_BEFORE)
        if settings.DEBUG: i.log.debug(f"TALG - condition=call_alpha: case={case}")
        return case

class CoverAlpha(fsm.Condition):
    def yes(self, i):
        case = i.claim(p.ALPHA_ALIAS)
        if settings.DEBUG: i.log.debug(f"TALG - condition=cover_alpha: case={case}")
        return case

class CallBeta(fsm.Condition):
    def yes(self, i):
        case = not i.claim(p.BETA_ALIAS) and i.datetime() <= u.today(p.TIME_STOP_CALL)
        if settings.DEBUG: i.log.debug(f"TALG - condition=call_beta: case={case}")
        return case

class CoverBeta(fsm.Condition):
    def yes(self, i):
        case = i.claim(p.BETA_ALIAS)
        if settings.DEBUG: i.log.debug(f"TALG - condition=cover_beta: case={case}")
        return case

class CallCharlie(fsm.Condition):
    def yes(self, i):
        case = not i.claim(p.CHARLIE_ALIAS) and i.datetime() <= u.today(p.TIME_STOP_CALL)
        if settings.DEBUG: i.log.debug(f"TALG - condition=call_charlie: case={case}")
        return case

class CoverCharlie(fsm.Condition):
    def yes(self, i):
        case = i.claim(p.CHARLIE_ALIAS)
        if settings.DEBUG: i.log.debug(f"TALG - condition=cover_charlie: case={case}")
        return case

################################################
################## Export(s) ###################
null = fsm.NoCondition()

### Trading Strategies
################################################
is_ready = IsReady()

### Call(s)
call_alpha = CallAlpha(ambiguous=False)
call_beta = CallBeta(ambiguous=False)
call_charlie = CallCharlie(ambiguous=False)

### Cover(s)
cover_alpha = CoverAlpha(ambiguous=False)
cover_beta = CoverBeta(ambiguous=False)
cover_charlie = CoverCharlie(ambiguous=False)
