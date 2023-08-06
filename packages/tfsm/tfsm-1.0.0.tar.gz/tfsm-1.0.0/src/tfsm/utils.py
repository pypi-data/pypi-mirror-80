# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
from datetime import date, datetime, timedelta
from pathlib import Path

from tfsm import settings as s


################################################
################## Function(s) #################

### Datetime Utility
################################################
today = lambda t: datetime.combine(date.today(), t).astimezone(s.TIME_ZONE)
tomorrow = lambda t: datetime.combine(date.today() + timedelta(days=1), t).astimezone(s.TIME_ZONE)
future = lambda t, days: datetime.combine(date.today() + timedelta(days=days), t).astimezone(s.TIME_ZONE)


### Condition(s)
################################################
market_is_open = lambda dt: dt.weekday() < s.DAY_OF_WEEK and today(s.TIME_PRE_MARKET) <= dt < today(s.TIME_POST_MARKET)
market_is_tradable = lambda dt: dt.weekday() < s.DAY_OF_WEEK and today(s.TIME_OPEN_MARKET) <= dt < today(s.TIME_CLOSE_MARKET)


### Directories
################################################
data_dir = lambda symbol, suffix="npy": Path.joinpath(s.DATA_DIR, f"{symbol}/data.{suffix}")
claims_dir = lambda symbol, suffix="npy": Path.joinpath(s.DATA_DIR, f"{symbol}/claims.{suffix}")
docs_dir = lambda symbol, suffix="npy": Path.joinpath(s.DATA_DIR, f"{symbol}/docs.{suffix}")
