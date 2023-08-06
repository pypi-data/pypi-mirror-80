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
################ Transition(s) #################
class Tick(fsm.Transition):
    def run(self, i):
        if i.datetime() > u.today(p.TIME_COVER_ALL): 
            i.note(p.ALPHA_ALIAS, i.metrics.cur())
        
        if settings.DEBUG: i.log.debug(f"TALG - transition=tick")

class CallAlpha(fsm.Transition):
    def run(self, i):
        strategy = p.ALPHA_ALIAS
        yesterday = i.probe(strategy)

        if yesterday:
            gap = (i.metrics.cur() - yesterday) / yesterday

            if gap <= p.ALPHA_GAP_LONG: i.call(strategy, models.Intent.LONG)
            elif gap >= p.ALPHA_GAP_SHORT: i.call(strategy, models.Intent.SHORT)
        
        if settings.DEBUG: i.log.debug(f"TALG - transition=call_alpha: strategy={strategy}, yesterday={yesterday}")

class CoverAlpha(fsm.Transition):
    def run(self, i):
        strategy = p.ALPHA_ALIAS
        claim = i.claim(strategy)
        
        delta = (i.metrics.cur() - claim.opening) / claim.opening
        if (
            i.datetime() > u.today(p.ALPHA_TIME_EXIT_AFTER)
        ) or (
            claim.intent == models.Intent.LONG and
            delta >= p.ALPHA_PROFIT_LONG
        ) or (
            claim.intent == models.Intent.SHORT and
            delta <= p.ALPHA_PROFIT_SHORT
        ): i.cover(strategy)

        if settings.DEBUG: i.log.debug(f"TALG - transition=cover_alpha: strategy={strategy}, delta={delta:.2f}")

class CallBeta(fsm.Transition):
    def run(self, i):
        strategy = p.BETA_ALIAS
        period = p.BETA_PERIOD

        if ( # crosses above SMA
            i.metrics.cur() > i.metrics.cur_sma(period) and 
            i.metrics.prv() <= i.metrics.prv_sma(period)
        ): i.call(strategy, models.Intent.LONG)
        elif ( # crosses below SMA
            i.metrics.cur() < i.metrics.cur_sma(period) and 
            i.metrics.prv() >= i.metrics.prv_sma(period)
        ): i.call(strategy, models.Intent.SHORT)

        if settings.DEBUG: i.log.debug(f"TALG - transition=call_beta: strategy={strategy}, period={period}")

class CoverBeta(fsm.Transition):
    def run(self, i):
        strategy = p.BETA_ALIAS
        period = p.BETA_PERIOD
        claim = i.claim(strategy)
        point = i.metrics.cur()
        sma = i.metrics.cur_sma(period)

        delta = (point - claim.opening) / claim.opening
        dsma = (point - sma) / sma
        if (
            i.datetime() > u.today(p.TIME_COVER_ALL)
        ) or (
            claim.intent == models.Intent.LONG and
            (
                dsma <= -p.THRESHOLD_DELTA_SMA or
                delta >= p.BETA_PROFIT_LONG or
                delta <= p.BETA_LOSS_LONG
            )
        ) or (
            claim.intent == models.Intent.SHORT and
            (
                dsma >= p.THRESHOLD_DELTA_SMA or
                delta <= p.BETA_PROFIT_SHORT or
                delta >= p.BETA_LOSS_SHORT
            )
        ): i.cover(strategy)

        if settings.DEBUG: i.log.debug(f"TALG - transition=cover_beta: strategy={strategy}, delta={delta:.2f}, dsma={dsma:.2f}")

class CallCharlie(fsm.Transition):
    def run(self, i):
        strategy = p.CHARLIE_ALIAS
        period = p.CHARLIE_PERIOD

        if ( # crosses above SMA
            i.metrics.cur() > i.metrics.cur_sma(period) and 
            i.metrics.prv() <= i.metrics.prv_sma(period)
        ): i.call(strategy, models.Intent.LONG)
        elif ( # crosses below SMA
            i.metrics.cur() < i.metrics.cur_sma(period) and 
            i.metrics.prv() >= i.metrics.prv_sma(period)
        ): i.call(strategy, models.Intent.SHORT)

        if settings.DEBUG: i.log.debug(f"TALG - Transition=call_charlie: strategy={strategy}, period={period}")

class CoverCharlie(fsm.Transition):
    def run(self, i):
        strategy = p.CHARLIE_ALIAS
        period = p.CHARLIE_PERIOD
        claim = i.claim(strategy)
        point = i.metrics.cur()
        sma = i.metrics.cur_sma(period)

        zone = i.probe(strategy)
        delta = (point - claim.opening) / claim.opening
        dsma = (point - sma) / sma
        if not zone:
            if (
                claim.intent == models.Intent.LONG and
                delta >= p.CHARLIE_PROFIT_LONG
            ) or (
                claim.intent == models.Intent.SHORT and
                delta <= p.CHARLIE_PROFIT_SHORT
            ): i.note(strategy, True); zone = True

        if (
            i.datetime() > u.today(p.TIME_COVER_ALL)
        ) or (
            claim.intent == models.Intent.LONG and
            (
                dsma <= -p.THRESHOLD_DELTA_SMA or
                delta <= p.CHARLIE_LOSS_LONG or
                (
                    zone and
                    (
                        delta >= p.CHARLIE_PROFIT_HI_LONG or
                        delta <= p.CHARLIE_PROFIT_LO_LONG
                    )
                )
            )
        ) or (
            claim.intent == models.Intent.SHORT and
            (
                dsma >= p.THRESHOLD_DELTA_SMA or
                delta >= p.CHARLIE_LOSS_SHORT or
                (
                    zone and
                    (
                        delta <= p.CHARLIE_PROFIT_HI_SHORT or
                        delta >= p.CHARLIE_PROFIT_LO_SHORT
                    )
                )
            )
        ): i.cover(strategy); i.pop(strategy)

        if settings.DEBUG: i.log.debug(f"TALG - transition=cover_charlie: strategy={strategy}, zone={zone}, delta={delta:.2f}, dsma={dsma:.2f}")

################################################
################## Export(s) ###################
null = fsm.NoTransition()

### Trading Strategies
################################################
tick = Tick()

### Call(s)
call_alpha = CallAlpha()
call_beta = CallBeta()
call_charlie = CallCharlie()

### Cover(s)
cover_alpha = CoverAlpha()
cover_beta = CoverBeta()
cover_charlie = CoverCharlie()
