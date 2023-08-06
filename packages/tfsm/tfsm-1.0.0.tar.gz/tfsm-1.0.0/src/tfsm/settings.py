# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import datetime
import pytz

from pathlib import Path

from tfsm import utils as u


################################################
################### Settings ###################

### Build paths inside the project like this: 
###   BASE_DIR / 'subdir'.
################################################
BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
DATA_DIR = Path.joinpath(BASE_DIR, "data/")

### SECURITY WARNING: don't run with debug 
###   turned on in production!
################################################
DEBUG = True
LEAN = False

### Internationalization
################################################
LANGUAGE_CODE = 'en-us'
TIME_ZONE = pytz.timezone('America/New_York')

### Stock exchange market information
################################################
DAY_OF_WEEK = 5

TIME_PRE_MARKET = datetime.time(4, 00, 0)
TIME_OPEN_MARKET = datetime.time(9, 30, 0)
TIME_CLOSE_MARKET = datetime.time(16, 00, 0)
TIME_POST_MARKET = datetime.time(20, 00, 0)

### Application settings
################################################
WAIT = 0.1 # in seconds

WINDOW = 12 # i.e. 12 historical, 1 live

RETENTION_PERIOD = 2 # days
DATA_PER_DAY = (u.today(TIME_CLOSE_MARKET) - u.today(TIME_OPEN_MARKET)).total_seconds() # seconds
FREQUENCY_OF_DATA = 1.0 # per second
PERIOD_OF_DATA = 1.0 / FREQUENCY_OF_DATA # seconds

SIZE_OF_DATA = int(FREQUENCY_OF_DATA * DATA_PER_DAY * RETENTION_PERIOD)
