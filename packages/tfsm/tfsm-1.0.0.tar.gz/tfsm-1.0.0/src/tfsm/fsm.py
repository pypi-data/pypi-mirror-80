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

from tfsm import exceptions, settings

"""An example of a State Table

[
    ( state_a, (condition_a, [transition_a ...], next_state_a) ),
    ( state_a, (condition_b, transition_b, next_state_b) ),
    ( state_b, (condition_c, transition_c, next_state_c) ),
    ( state_c, (condition_d, [transition_d ...], next_state_b) ),
    ...
]

"""


################################################
############# Finite State Machine #############
class State:
    def __init__(self, name): self.name = name
    
    def __str__(self): return self.name
    def __lt__(self, other): return self.name < other.name
    def __gt__(self, other): return self.name > other.name
    def __le__(self, other): return self.name <= other.name
    def __ge__(self, other): return self.name >= other.name
    def __eq__(self, other): return self.name == other.name
    def __ne__(self, other): return self.name != other.name
    # Necessary when __lt__ and __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.name)

class Input:
    def __init__(self): 
        self.log = logging
        if settings.DEBUG: 
            self.log.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s")
        else: self.log.basicConfig(level=logging.WARN, format="%(name)s - %(levelname)s - %(message)s")
        
class Condition:
    def __init__(self, ambiguous=True):
        self.ambiguous = ambiguous
    
    def is_ambiguous(self): return self.ambiguous
    def is_unambiguous(self): return not self.ambiguous
    def yes(self, i): assert(0, "succeed() not implemented")
    def no(self, i): return not self.yes(i)

class NoCondition(Condition):
    def yes(self, i): return True

class Transition:
    def run(self, i): assert(0, "run() not implemented")

class NoTransition:
    def run(self, i): pass

class StateMachine:
    def __init__(self, name, initial_state, state_table):
        self.name = name
        self.initial_state = initial_state
        self.state_table = {}
        for key, value in state_table:
            if len(value) == 3:
                value = ( [ (value[0], value[1]) ], value[2] )
            
            if key in self.state_table:
                self.state_table[key].append(value)
            else:
                self.state_table[key] = [value]

    # Template method(s):
    def deflected(self, threads, i):
        for thread in threads:
            condition, transitions = thread
            
            if condition.is_ambiguous(): # i.e. multiple possible states available
                if condition.no(i): 
                    return True # i.e. deflect and route elsewhere
            else:
                if condition.no(i): 
                    continue # i.e. move to the next condition, if any
            
            if type(transitions) == list:
                for transition in transitions:
                    transition.run(i)
            else: transitions.run(i)
        
        return False

    def next_state(self, key, i):
        if settings.DEBUG: i.log.debug(f"{self.name} - state={key.name}")

        values = self.state_table.get(key)
        for value in values:
            threads, state = value

            if self.deflected(threads, i): 
                continue # i.e. move to the next condition, if any
            
            return state, i

        if key.name.lower() != "end": 
            raise exceptions.StateMachineError("Invalid 'state_table'.", (self, i))
        
        return key, i

    def run(self, i):
        state = self.initial_state
        
        while state.name.lower() != "end":
            state, i = self.next_state(state, i)
