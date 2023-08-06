# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################## Import(s) ###################
import datetime
import logging
import numpy as np
import random
import tulipy as ti

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from tfsm import fsm, settings, utils


################################################
################### Model(s) ###################
class Brokerage:
    # TODO: make an identification system i.e. passport, dt_expiry, etc.
    # TODO: send the requests i.e. big, ask, etc. register, refresh ...
    def __init__(self):
        self.passport = None
        self.dt_expiry = None

    def live(self, symbol, mock=None): 
        if settings.LEAN and mock: return mock

        response = {
            "symbol": symbol,
            "time": "2019-01-01 14:23:42",
            "bid": random.uniform(150.0, 250.0),
            "ask": random.uniform(150.0, 250.0),
            "last": random.uniform(150.0, 250.0),
            "volume": random.randint(1, 100),
            "open": random.uniform(150.0, 250.0),
            "high": random.uniform(150.0, 250.0),
            "low": random.uniform(150.0, 250.0),
            "close": random.uniform(150.0, 250.0)
        }
        return response
    
    def bid(self, symbol, volume, bid): # i.e. buy
        if type(bid) == dict: bid = bid["bid"]
        
        print(f"request bid: symbol={symbol}, volume={volume}, bid=${bid}")
        return bid

    def ask(self, symbol, volume, ask): # i.e. sell
        if type(ask) == dict: ask = ask["ask"]

        print(f"request ask: symbol={symbol}, volume={volume}, ask=${ask}")
        return ask

class Intent(Enum):
    LONG = 1
    SHORT = 2

    def __str__(self): return self.name

class Leg(Enum):
    CALL = 1
    COVER = 0
    
    def __str__(self): return self.name
    
@dataclass
class Claim:
    symbol: str
    intent: Intent
    volume: int
    opening: float
    closing: float = None

    # == Meta-Information ==
    leg: Leg = Leg.CALL

    # == Flag(s) ==
    is_active: bool = True  # was this claim renewed this clock cycle?
    
    def __str__(self): 
        if self.closing:
            return f"{self.intent}:{self.volume}x{self.symbol}@${self.opening:.2f}~>${self.closing:.2f}"
        else: return f"{self.intent}:{self.volume}x{self.symbol}@${self.opening:.2f}"

class Metrics:
    def __init__(self, symbol, log=None):
        if not log: 
            self.log = logging
            self.log.basicConfig(level=logging.WARN, format="%(name)s - %(levelname)s - %(message)s")
        else: self.log = log
        
        self.symbol = symbol
        self.load()
        self.install()

    # == Setup ==
    def save(self):
        # 1. path
        data_path = utils.data_dir(self.symbol)
        
        # 2. mkdir
        Path(data_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 3. save
        np.save(data_path, self.__data)
    
    def load(self):
        data_path = utils.data_dir(self.symbol)

        if Path.exists(data_path):
            self.__data = np.load(data_path, allow_pickle=True)

            sum_empty = np.sum([not bool(point) for point in self.__data])
            if settings.SIZE_OF_DATA >= sum_empty:
                self.__size = settings.SIZE_OF_DATA - sum_empty
            else: self.__size = settings.SIZE_OF_DATA
        
        else:
            self.__data = np.full(settings.SIZE_OF_DATA, dict(), dtype=dict)
            self.__size = 0

        if settings.DEBUG: 
            self.log.debug(f"Metrics - load: __size={self.__size}")
            self.log.debug(f"\t__data={self.__data[:1]} ...")
            self.log.debug(f"\t... {self.__data[-1:]}")

    def install(self):
        self.__options = {
            "ema": self.shift_ema,
            "sma": self.shift_sma
        }
        self.__periods = [
            int(settings.FREQUENCY_OF_DATA * 300), 
            int(settings.FREQUENCY_OF_DATA * 3600)
        ]

        for option in self.__options.keys():
            setattr(self, f"{option}s", dict())
            for period in self.__periods:
                size_metric = settings.SIZE_OF_DATA - settings.WINDOW * period
                if size_metric < 1: size_metric = 1
                getattr(self, f"{option}s")[period] = np.full(size_metric, np.nan)
            
        for index in range(2): self.calculate(index=index)
    
    # == Utility ==
    def select(self, point, attr="close"): return point[attr]
    def snippet(self, period, index=0, reverse=False):
        if reverse: 
            spread = np.arange(settings.WINDOW * period + index, index - 1, -period)
        else: spread = np.arange(index, settings.WINDOW * period + index + 1, period)
        return np.array([self.select(point) for point in self.__data[spread] if bool(point)])
    
    def show(self):
        self.log.info("Metrics - show():")
        for index, option in enumerate(self.__options.keys()):
            self.log.info(f"\t{index+1}. {option}")
            indicator = getattr(self, f"{option}s")
            
            for period in self.__periods:
                figures = indicator[period]
                self.log.info(f"\t  {period}: len={len(figures)}, figures={figures[:2]} ... {figures[-2:]}")

    # == Setter(s) ==
    def full(self, mock):
        self.__data = np.full(settings.SIZE_OF_DATA, mock, dtype=dict)
    
    def bulk(self, data):
        # Assumption: len(data) == settings.SIZE_OF_DATA
        self.__data[:] = data

    def append(self, point):
        self.shift(point)
        self.__size += 1
    
    def shift(self, point, N=1):
        self.__data[N:] = self.__data[:-N]
        self.__data[:N] = point

    # == Getter(s) ==
    def data(self): return self.__data
    def size(self): return self.__size
    def len(self, attr): 
        if attr[-1] != 's': attr = attr + 's'
        attr = attr.lower()

        result = {}

        indicator = getattr(self, attr)
        for period in self.__periods:
            figures = indicator[period]

            size = len(figures)
            sum_nan = np.isnan(figures).sum()
            if size >= sum_nan:
                result[period] = size - sum_nan
            else: result[period] = size

        return result
    
    def point(self, index, select=True): 
        if select: 
            return self.select(self.__data[index])
        else: return self.__data[index]
    def cur(self, select=True): return self.point(0, select)
    def prv(self, select=True): return self.point(1, select)

    # == Functional ==
    def calculate(self, indicators=None, index=0):
        if not indicators: indicators = self.__options.keys()
        for indicator in indicators:
            self.__options[indicator](index=index)

    # == Indicator(s) ==
    def shift_sma(self, index=0, N=1):
        for period in self.__periods:
            arr = self.snippet(period, index=index)
            
            if len(arr) > settings.WINDOW:
                sma = ti.sma(arr, period=settings.WINDOW+1)
                self.smas[period][N:] = self.smas[period][:-N]
                self.smas[period][:N] = sma
    
    def shift_ema(self, index=0, N=1):
        for period in self.__periods:
            arr = self.snippet(period, index=index, reverse=True)
            
            if len(arr) > settings.WINDOW:
                # TODO: confirm Tuplip EMA w/ James
                ema = ti.ema(arr, period=settings.WINDOW+1)[-1]
                self.emas[period][N:] = self.emas[period][:-N]
                self.emas[period][:N] = ema
    
    def sma(self, period, index): return self.smas[period][index]
    def ema(self, period, index): return self.emas[period][index]
    def cur_sma(self, period): return self.sma(period, 0)
    def cur_ema(self, period): return self.ema(period, 0)
    def prv_sma(self, period): return self.sma(period, 1)
    def prv_ema(self, period): return self.ema(period, 1)

class TfsmInput(fsm.Input):
    def __init__(self, symbol, timezone):
        super().__init__()
        self.symbol = symbol
        self.timezone = timezone

        self.ready = False
        self.load()
        
    def __str__(self): return self.symbol
    def __lt__(self, other): return self.dt_talg < other.dt_talg
    def __gt__(self, other): return self.dt_talg > other.dt_talg
    def __le__(self, other): return self.dt_talg <= other.dt_talg
    def __ge__(self, other): return self.dt_talg >= other.dt_talg
    def __eq__(self, other): return self.dt_talg == other.dt_talg
    def __ne__(self, other): return self.dt_talg != other.dt_talg
    # Necessary when __lt__ and __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.symbol)
    
    # == Setup ==
    def save(self):
        # = Externally Managed Module(s) =
        self.metrics.save()

        # = Internally Managed Module(s) =
        # 1. path
        claims_path = utils.claims_dir(self.symbol)
        docs_path = utils.docs_dir(self.symbol)
        
        # 2. mkdir
        Path(claims_path).parent.mkdir(parents=True, exist_ok=True)
        Path(docs_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 3. save
        np.save(claims_path, self.__claims)
        np.save(docs_path, self.__docs)
        
    def load(self):
        # = Externally Managed Module(s) =
        self.broker = Brokerage()
        self.metrics = Metrics(self.symbol, log=self.log)
        
        # = Internally Managed Module(s) =
        # 1. path
        claims_path = utils.claims_dir(self.symbol)
        docs_path = utils.docs_dir(self.symbol)
        
        # 2. load
        # ~> claims
        if Path(claims_path).exists():
            self.__claims = np.load(claims_path, allow_pickle=True).item()
        else: self.__claims = dict()

        # ~> docs
        if Path(docs_path).exists():
            self.__docs = np.load(docs_path, allow_pickle=True).item()
        else: self.__docs = dict()

        if settings.DEBUG: self.show()
        self.dt_talg = datetime.datetime.now(self.timezone)
        self.dt_tsys = self.dt_talg.replace(microsecond=0)
    
    # == Functional ==
    # = TSYS =
    def clock(self, tick=False):
        now = datetime.datetime.now(self.timezone)
        if tick: 
            self.dt_talg = now
        else: self.dt_tsys = self.dt_tsys + datetime.timedelta(seconds=settings.PERIOD_OF_DATA)
        
        return now, self.dt_tsys

    def get(self, symbol=None, mock=None):
        if not symbol: 
            symbol = self.symbol
        
        self.stash = self.broker.live(symbol, mock)
        return self.stash
    
    # = TALG =
    def refresh(self):
        # ~> Claim(s)
        rms = list()
        for key, val in self.__claims.items():
            if val.leg == Leg.COVER: 
                rms.append(key)
            else: self.__claims[key].is_active = False

        for rm in rms: self.__claims.pop(rm, None)

    def tick(self):
        if self.metrics.size() < settings.SIZE_OF_DATA:
            self.metrics.append(self.stash)
        else: 
            if not self.ready: 
                self.ready = True
            self.metrics.shift(self.stash)
            
        self.metrics.calculate()
        self.refresh()

        return self.clock(tick=True)

    def call(self, strategy, intent, volume=1, amount=None):
        strategy = strategy.lower()
        if not amount: amount = self.metrics.cur(select=False)

        if intent == Intent.LONG:
            amount = self.broker.bid(self.symbol, volume, amount)
        elif intent == Intent.SHORT:
            amount = self.broker.ask(self.symbol, volume, amount)

        self.__claims[strategy] = Claim(self.symbol, intent, volume, amount)
    
    def cover(self, strategy, amount=None):
        strategy = strategy.lower()
        if not amount: amount = self.metrics.cur(select=False)

        claim = self.__claims.pop(strategy, None)

        if claim.intent == Intent.LONG:
            amount = self.broker.ask(claim.symbol, claim.volume, amount)
        elif claim.intent == Intent.SHORT:
            amount = self.broker.bid(claim.symbol, claim.volume, amount)

        claim.closing = amount
        claim.leg = Leg.COVER
        claim.is_active = True
        self.__claims[strategy] = claim

    # == Utility ==
    def datetime(self): return datetime.datetime.now(tz=self.timezone)
    def show(self):
        # = Externally Managed Module(s) =
        self.metrics.show()

        # = Internally Managed Module(s) =
        self.log.info("TfsmInput - show():")
        self.log.info("Doc(s):")
        for key, val in self.__docs.items():
            self.log.info(f"\t{key}={val}")

        self.log.info("Claim(s):")
        for index, key in enumerate(self.__claims.keys()):
            claim = self.__claims[key]
            self.log.info(f"\t{index+1}. {key}={claim}")

    # == Setter(s) ==
    def note(self, key, message): self.__docs[key.lower()] = message
    def pop(self, key): return self.__docs.pop(key.lower(), None)
    
    # == Getter(s) ==
    def probe(self, key): return self.__docs.get(key.lower(), None)

    def claim(self, strategy): return self.__claims.get(strategy.lower(), None)
    def claims(self): return self.__claims.values()
    def active_claims(self): return [claim for claim in self.__claims.values() if claim.is_active == True]
    def strategies(self): return self.__claims.keys()
    