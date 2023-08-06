# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

from __future__ import unicode_literals, absolute_import

################################################
################## Import(s) ###################
from tfsm import exceptions, fsm, models, settings, utils


################################################
################## Export(s) ###################
from tfsm.machines import tsys
from tfsm.machines import talg


### Machine(s)
################################################
def build_tsys():
    initial_state = tsys.S.start
    state_table = [
        # === ( STATE, ( CONDITION, [TRANSITION...], NEXT_STATE ) )
        # === ( STATE, ( [ (CONDITION, [TRANSITION...])... ], NEXT_STATE ) )
        # = a) Start
        ( tsys.S.start, (tsys.C.null, tsys.T.null, tsys.S.connect) ),

        # = b) Connect
        ( tsys.S.connect, (tsys.C.ai_is_not_registered, tsys.T.register, tsys.S.connect) ),
        ( tsys.S.connect, (tsys.C.service_about_to_expire, tsys.T.refresh, tsys.S.connect) ),
        ( tsys.S.connect, (tsys.C.market_is_open, tsys.T.get, tsys.S.market) ),
        ( tsys.S.connect, (tsys.C.null, tsys.T.wait, tsys.S.connect) ),

        # = c) Market
        ( tsys.S.market, (tsys.C.response_is_valid, tsys.T.tick, tsys.S.tick) ),
        ( tsys.S.market, (tsys.C.null, tsys.T.null, tsys.S.connect) ),

        # = d) Tick
        ( tsys.S.tick, (tsys.C.market_is_tradable, tsys.T.null, tsys.S.algorithm) ),
        ( tsys.S.tick, (tsys.C.null, tsys.T.delay, tsys.S.connect) ),

        # = e) Algorithm
        ( tsys.S.algorithm, (tsys.C.null, tsys.T.delay, tsys.S.connect) )
    ]

    return fsm.StateMachine("TSYS", initial_state, state_table)

def build_talg():
    initial_state = talg.S.start
    state_table = [
        # === ( STATE, ( CONDITION, [TRANSITION...], NEXT_STATE ) )
        # === ( STATE, ( [ (CONDITION, [TRANSITION...])... ], NEXT_STATE ) )
        # = a) Start
        ( talg.S.start, (talg.C.is_ready, talg.T.tick, talg.S.covers) ),
        ( talg.S.start, (talg.C.null, talg.T.tick, talg.S.end) ),

        # = b) Covers
        (
            talg.S.covers,
            (
                [
                    (talg.C.cover_alpha, talg.T.cover_alpha),
                    (talg.C.cover_beta, talg.T.cover_beta),
                    (talg.C.cover_charlie, talg.T.cover_charlie)
                ],
                talg.S.calls
            )
        ),

        # = c) Calls
        (
            talg.S.calls,
            (
                [
                    (talg.C.call_alpha, talg.T.call_alpha),
                    (talg.C.call_beta, talg.T.call_beta),
                    (talg.C.call_charlie, talg.T.call_charlie)
                ],
                talg.S.end
            )
        )
    ]

    return fsm.StateMachine("TALG", initial_state, state_table)
