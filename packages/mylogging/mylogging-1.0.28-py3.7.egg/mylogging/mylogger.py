"""
My python logging module. Based on debug value prints warnings and errors. It's automatically colorized. It can be logged to file if configured.

Documentation does not exists, because it's such a small project, that it's not necessary.

Motivation for this project is, that i need this functionallity in each project, so to not repeat myself.

## Example

```python

>>> from mylogging import mylogger

>>> mylogger._COLORIZE = 0  # Turn on colorization on all functions

As set_warnings parameter we can define whether to
   display warnings: debug=1,
   ignore warnings: debug=0,
   stop warnings as errors: debug=3
Beware, that even if no warnings are configured, default warning setings are applied - so warning settings can be overwriten

>>> mylogger.set_warnings(debug=1, ignored_warnings=["invalid value encountered in sqrt",
                                                 "encountered in double_scalars"])

We can create warning that will be displayed based on warning settings

>>> mylogger.user_warning('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

# In case we don't know exact error reason, we can use traceback_warning in try/except block

>>> try:
>>>     u = 10 / 0

>>> except Exception:
>>>     mylogger.traceback_warning("Maybe try to use something different than 0")

# In case we don't want to warn, but we have error that should be printed anyway and not based on warning settings, we can use user_message that return extended that we can use...

>>> print(mylogger.user_message("I will be printed anyway"))
```

Check oficial repo for how the results look like. Warning messages are

If you want to log warnings into text file or it will be printed for example on some CI log console, colors will be probably changed into unwanted symbols. For such a cases you can use this after the import

>>> mylogger._COLORIZE = 0  # Turn off colorization on all functions
"""

import warnings
import traceback
import textwrap
import os
import pygments
from pygments.lexers import PythonTracebackLexer
from pygments.formatters import Terminal256Formatter

_COLORIZE = 1  # Whether colorize results - mostly python syntax in tracebacks.

### TODO - not implemented yet
_TO_FILE = 0  # Whether print or write to file.

# To enable colors in cmd...
os.system('')

# Debug value can be inserted as set_warnings argumnt. If not, default value will be used.
debug = 1  # If 1, print all the warnings and errors on the way, if 2, stop on first warning, if -1 do not print anything.


def user_warning(message, caption="User message", color='default'):
    """Raise warning - just message, not traceback. Can be colorized. Display of warning is based on warning settings.
    You can configure warning with function set_warnings with debug parameter.

    Args:
        message (str): Any string content of warning.
        caption (ctr): Headning of warning.
        color (bool): Whether colorize warning.
    """

    if color == 'default':
        color = _COLORIZE

    warnings.warn(user_message(message, caption=caption, color=color))


def traceback_warning(caption='Traceback warning', color='default'):
    """Raise warning with current traceback as content. There is many models in this library and with some
    configuration some models crashes. Actually it's not error than, but warning. Display of warning is
    configured with debug variable in `config.py`.

    Args:
        caption (str, optional): Caption of warning. Defaults to 'Traceback warning'.
    """
    if color == 'default':
        color = _COLORIZE

    if color:
        separated_traceback = pygments.highlight(traceback.format_exc(), PythonTracebackLexer(), Terminal256Formatter(style='friendly'))
    else:
        separated_traceback = traceback.format_exc()

    # separated_traceback = textwrap.indent(text=f"\n\n{message}\n====================\n\n{separated_traceback}\n====================\n", prefix='    ')
    separated_traceback = user_message(message=separated_traceback, caption=caption, around=True)

    warnings.warn(f"\n\n\n{separated_traceback}\n\n")


def set_warnings(debug=debug, ignored_warnings=[]):
    """Define debug type. Can print warnings, ignore them or stop as error

    Args:
        debug (int): If 0, than warnings are ignored, if 1, than warning will be displayed just once, if 2,
            program raise error on warning and stop.
        ignored_warnings (list): List of warnings (any part of inner string) that will be ingored even if debug is set.
    """

    if debug == 1:
        warnings.filterwarnings('once')
    elif debug == 2:
        warnings.filterwarnings('error')
    else:
        warnings.filterwarnings('ignore')

    for i in ignored_warnings:
        warnings.filterwarnings('ignore', message=fr"[\s\S]*{i}*")


def user_message(message, caption="User message", around=False, color='default'):
    """Return enhanced colored message. Used for raising exceptions, assertions or important warninfs mainly.
    You can print returned message, or you can use user_warning function. Then it will be printed only in debug mode.

    Args:
        message (str): Any string content of warning.
        caption (ctr): Headning of warning.

    Returns:
        str: Enhanced message as a string, that is wrapped by and can be colorized.
    """
    if color == 'default':
        color = _COLORIZE

    updated_str = textwrap.indent(
        text=f"\n\n========= {caption} ========= \n\n {message} \n\n",
        prefix='    ')

    if color:
        updated_str = colorize(updated_str)

    # Have to be separatedly because otherwise bottom margin get no colored in tracebacks
    if around:
        if color:
            updated_str = updated_str + textwrap.indent(colorize(f"{'=' * (len(caption) + 20) if around else ''} \n\n\n"), prefix='    ')
        else:
            updated_str = updated_str + textwrap.indent(f"{'=' * (len(caption) + 20) if around else ''} \n\n\n", prefix='    ')

    return objectize_str(updated_str)


def objectize_str(message):
    """Make a class from a string to be able to apply escape characters and colors in tracebacks.

    Args:
        message (str): Any string you use.

    Returns:
        Object: Object, that can return string if printed or used in warning or raise.
    """
    class X(str):
        def __repr__(self):
            return f"{message}"

    return X(message)


def colorize(message):
    """Add color to message - usally warnings and errors, to know what is internal error on first sight.
    Simple string edit.

    Args:
        message (str): Any string you want to color.

    Returns:
        str: Message in yellow color. Symbols added to string cannot be read in some terminals.
            If global _COLORIZE is 0, it return original string.
    """

    return f"\033[93m {message} \033[0m"


set_warnings()
