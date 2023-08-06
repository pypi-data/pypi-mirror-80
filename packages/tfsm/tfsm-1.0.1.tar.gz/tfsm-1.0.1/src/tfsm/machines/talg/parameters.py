# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import datetime

from tfsm import settings


################################################
################## Parameters ##################

### Generic
################################################
TIME_STOP_CALL = datetime.time(15, 59, 0)
TIME_COVER_ALL = datetime.time(15, 59, 55)


### Alpha
################################################
ALPHA_ALIAS = "alpha"

###~> Entry
ALPHA_TIME_ENTER_BEFORE = datetime.time(9, 30, 3)
ALPHA_GAP_LONG = -0.05
ALPHA_GAP_SHORT = 0.05

###~> Exit
ALPHA_TIME_EXIT_AFTER = datetime.time(9, 35, 0)
ALPHA_PROFIT_LONG = 0.02
ALPHA_PROFIT_SHORT = -0.02


### Beta
################################################
BETA_ALIAS = "beta"
BETA_PERIOD = int(settings.FREQUENCY_OF_DATA * 300)

###~> Entry
###~> Exit
THRESHOLD_DELTA_SMA = 0.01

BETA_PROFIT_LONG = 0.03
BETA_PROFIT_SHORT = -0.025

BETA_LOSS_LONG = -0.02
BETA_LOSS_SHORT = 0.015


### Charlie
################################################
CHARLIE_ALIAS = "charlie"
CHARLIE_PERIOD = int(settings.FREQUENCY_OF_DATA * 3600)

###~> Entry
###~> Exit
CHARLIE_PROFIT_LONG = 0.03
CHARLIE_PROFIT_SHORT = -0.03

CHARLIE_PROFIT_HI_LONG = 0.06
CHARLIE_PROFIT_HI_SHORT = -0.06

CHARLIE_PROFIT_LO_LONG = 0.02
CHARLIE_PROFIT_LO_SHORT = -0.02

CHARLIE_LOSS_LONG = -0.02
CHARLIE_LOSS_SHORT = 0.02
