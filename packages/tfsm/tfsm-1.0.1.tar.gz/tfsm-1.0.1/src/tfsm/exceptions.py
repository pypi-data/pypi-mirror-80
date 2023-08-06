# coding=utf-8
#
# tfsm - Trader Finite State Machine
#
# Copyright (C) 2020 Edward Liu <edwardy.liu@mail.utoronto.ca>
#

################################################
################# Exception(s) #################
class TfsmError(Exception):
    """The base class for exceptions raised in the 'tfsm' module"""
    pass

class StateError(TfsmError):
    """Exception raised for errors in the state.

    Attributes:
        message -- explanation of the error
        expression -- state expression in which the error occurred
    """

    def __init__(self, message, expression):
        self.message = message
        self.expression = expression

class InputError(TfsmError):
    """Exception raised for errors in the input.

    Attributes:
        message -- explanation of the error
        expression -- input expression in which the error occurred
    """

    def __init__(self, message, expression):
        self.message = message
        self.expression = expression

class ConditionError(TfsmError):
    """Exception raised for errors in the condition.

    Attributes:
        message -- explanation of the error
        expression -- condition expression in which the error occurred
    """

    def __init__(self, message, expression=None):
        self.message = message
        self.expression = expression

class TransitionError(TfsmError):
    """Exception raised for errors in the transition.

    Attributes:
        message -- explanation of the error
        expression -- transition expression in which the error occurred
    """

    def __init__(self, message, expression=None):
        self.message = message
        self.expression = expression

class StateMachineError(TfsmError):
    """Exception raised for errors in the state machine.

    Attributes:
        message -- explanation of the error
        expression -- state machine expression in which the error occurred
    """

    def __init__(self, message, expression=None):
        self.message = message
        self.expression = expression
