# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import time

from tfsm import exceptions, fsm, models, settings, utils as u


################################################
################ Transition(s) #################
class Register(fsm.Transition):
    def run(self, i):
        # TODO: send request, get response, update
        if settings.DEBUG: i.log.debug("TSYS - transition=register")

class Refresh(fsm.Transition):
    def run(self, i):
        # TODO: send request, get response, update
        if settings.DEBUG: i.log.debug("TSYS - transition=refresh")

class Wait(fsm.Transition):
    def run(self, i):
        time.sleep(settings.WAIT)
        if settings.DEBUG: i.log.debug(f"TSYS - transition=wait: wait={settings.WAIT}s")

class Get(fsm.Transition):
    def run(self, i):
        stash = i.get()
        if settings.DEBUG: i.log.debug(f"TSYS - transition=get: stash={stash}")

class Tick(fsm.Transition):
    def run(self, i):
        i.tick()
        if settings.DEBUG: i.log.debug("TSYS - transition=tick")

class Delay(fsm.Transition):
    def run(self, i):
        dt_talg, dt_tsys = i.clock()
        delay = (dt_tsys - dt_talg).total_seconds()
        if delay > 0.: time.sleep(delay)
        
        if settings.DEBUG: i.log.debug(f"TSYS - transition=delay: delay={delay}s")


################################################
################## Export(s) ###################
null = fsm.NoTransition()

register = Register()
refresh = Refresh()
wait = Wait()
get = Get()
tick = Tick()
delay = Delay()
