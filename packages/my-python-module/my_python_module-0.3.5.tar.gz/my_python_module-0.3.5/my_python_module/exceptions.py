#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python系统内的异常
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
"""


class ConfigFileNotFoundError(FileNotFoundError):
    """
    The config file not found.
    """


class RequireArgumentError(Exception):
    """
    Require some argument
    """


class FatalError():
    """Fatal Error, the program need shutdown imediately"""


class NotIntegerError(ValueError):
    """Need input is a integer"""


class NotFloatError(ValueError):
    """Need input is a float"""


class OutOfRangeError(ValueError):
    """The input required a range"""


class OutOfChoiceError(ValueError):
    """The parameter is out of given choice"""


class NotSupportedWarning(UserWarning):
    """This feature is not supported, program will ignore it."""


class UnDefinedError():
    """UndefinedError, lately we will talk about it. """


class GraphError(Exception):
    """
    A base-class for the various kinds of errors that occur in the the graph class.
    """
    pass

class TreeError(Exception):
    """
    A base-class for the various kinds of errors that occur in the the tree class.
    """

class AdditionError(GraphError):
    """
    This error is raised when trying to add a node or edge already added
    to the graph or digraph.
    """
    pass


class NotAcyclicError(GraphError):
    """
    not acyclic graph error
    """
    pass


class GuessFailed(Warning):
    """
    Your function do some guess operation but cause a failed, this is a warning.
    """
