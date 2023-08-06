# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
from tfsm import exceptions, fsm, models, settings, utils as u


################################################
################# Condition(s) #################
class AiIsNotRegistered(fsm.Condition):
    def yes(self, i):
        # TODO: check UID, None on __init__
        case = False
        if settings.DEBUG: i.log.debug(f"TSYS - condition=ai_is_not_registered: case={case}")
        return case

class ServiceAboutToExpire(fsm.Condition):
    def yes(self, i): 
        # TODO: check expiry datetime
        case = False
        if settings.DEBUG: i.log.debug(f"TSYS - condition=service_about_to_expire: case={case}")
        return case

class MarketIsOpen(fsm.Condition):
    def yes(self, i):
        now = i.datetime()
        case = u.market_is_open(now)
        if settings.DEBUG: i.log.debug(f"TSYS - condition=market_is_open: now={now}, case={case}")
        return case

class ResponseIsValid(fsm.Condition):
    def yes(self, i):
        # TODO: validate response i.e. i.stash
        case = bool(i.stash)
        if settings.DEBUG: i.log.debug(f"TSYS - condition=response_is_valid: case={case}")
        return case

class MarketIsTradable(fsm.Condition):
    def yes(self, i):
        now = i.datetime()
        case = u.market_is_tradable(now)
        if settings.DEBUG: i.log.debug(f"TSYS - condition=market_is_tradable: now={now}, case={case}")
        return case

################################################
################## Export(s) ###################
null = fsm.NoCondition()

ai_is_not_registered = AiIsNotRegistered()
service_about_to_expire = ServiceAboutToExpire()
market_is_open = MarketIsOpen()
response_is_valid = ResponseIsValid()
market_is_tradable = MarketIsTradable()
