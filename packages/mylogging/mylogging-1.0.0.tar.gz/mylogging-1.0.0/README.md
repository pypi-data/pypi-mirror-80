# mylogging

My python logging module. Based on debug value prints warnings and errors. It's automatically colorized. It can be logged to file if configured.

Documentation does not exists, because it's such a small project, that it's not necessary.

Motivation for this project is, that i need this functionallity in each project, so to not repeat myself.

## Example

```python

from mylogging import mylogger

mylogger._COLORIZE = 0  # Turn on colorization on all functions

# We can define whether to
#   display warnings: debug=1,
#   ignore warnings: debug=0,
#   stop warnings as errors: debug=3
# Beware, that even if no warnings are configured, default warning setings are applied - so warning settings can be overwriten

mylogger.set_warnings(debug=1, ignored_warnings=["invalid value encountered in sqrt",
                                                 "encountered in double_scalars"])

# We can create warning that will be displayed based on warning settings
mylogger.user_warning('Hessian matrix copmputation failed for example', caption="RuntimeError on model x")

# In case we don't know exact error reason, we can use traceback_warning in try/except block

try:
    u = 10 / 0

except Exception:
    mylogger.traceback_warning("Maybe try to use something different than 0")

# In case we don't want to warn, but we have error that should be printed anyway and not based on warning settings, we can use user_message that return extended that we can use...

print(mylogger.user_message("I will be printed anyway"))
```

This is the result of the upper snippet

<p align="center">
<img src="logging.png" width="620" alt="Plot of results"/>
</p>

If you want to log warnings into text file or it will be printed for example on some CI log console, colors will be probably changed into unwanted symbols. For such a cases you can use this after the import

```python
mylogger._COLORIZE = 0  # Turn off colorization on all functions
```
