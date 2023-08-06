# Shortcutter

[![Build Status](https://travis-ci.org/kiwi0fruit/shortcutter.svg?branch=master)](https://travis-ci.org/kiwi0fruit/shortcutter)

Shortcutter is a cross platform API for creating shortcuts for python applications meant to be used in setup.py script or as a command line application (fork of the Shortcut).

Shortcutter creates shortcucts that activate python environment prior launching the app (activation can be disabled if needed). It supports virtual environments, Anaconda/Miniconda, conda environments, `sudo pip install`, `pip install --user`. Shortcutter will do its best to find your app, searching for the usual suspects in the usual places (i.e. those in the PATH), or you can give it a full path.

_**Shortcutter is intended to be used for click/drag'n'drop usage of shortcuts only. Hence do not call/source shortcutter wrapper scripts. If you need executable wrappers from activated environments see [exec-wrappers](https://github.com/gqmelo/exec-wrappers).**_  
But do not call/source them either - use `"%COMSPEC%" /c ".\path\to\execwrapper.bat" arg` (`call path-cmd.bat execwrapper arg` if it's in the PATH; see [this](https://github.com/kiwi0fruit/shortcutter/blob/master/path-cmd.bat)) on Windows and`"./path/to/execwrapper" arg` on Unix (`execwrapper arg` if it's in the PATH).

Additioanlly special command/method can create shortcut to the terminal at activated environment (plus terminal shortcut at conda root). In case of Windows special env vars `%u%` and `%a%` defined that switch encodings and `%b%` var that sets UTF-8 encoding and starts Bash.

To create desktop and menu shortcuts for `python`:

* Using the app:

```
shortcutter python
shortcutter --terminal
```

* Using the Python API for example in `setup.py`:

```py
from shortcutter import ShortCutter
sc = ShortCutter()
sc.create_desktop_shortcut("python")
sc.create_menu_shortcut("python")
sc.create_shortcut_to_env_terminal()
```

It was created to solve a simple problem - if you install a python package using `pip` there is no simple way of creating a shortcut to the program it installs.


## Shortcuts without entry points (for GUI)

The default use-case for Shortcutter is to create shortcuts for entry-points executables auto created by setup.py or conda. But sometimes such entry-points do not work (like when using pythonw on macOS with python.app package). See example how to work-around this: [Enaml video app](https://github.com/kiwi0fruit/enaml-video-app) (the main idea is in [bash](https://github.com/kiwi0fruit/enaml-video-app/blob/master/enaml-video-app/scripts/enaml-video-appw) script).


# Table of contents

* [Shortcutter](#shortcutter)
  * [Shortcuts without entry points (for GUI)](#shortcuts-without-entry-points-for-gui)
* [Install](#install)
* [Command line interface](#command-line-interface)
* [Python API](#python-api)
* [Operating Systems](#operating-systems)
* [Status](#status)
* [Change log](#change-log)


# Install

Shortcut is available on [pypi](https://pypi.python.org/pypi/shortcutter) and can be installed using `pip`:

* Using Anaconda/Miniconda:

```bat
conda install -c defaults -c conda-forge shortcutter
```

* Using pip:

```
pip install shortcutter
```

* System Python 3 on macOS or Linux:

```
pip3 install shortcutter
```

Note: if `pip3 install --user` (simply `pip3 install` on Ubuntu) then you might need to add `%APPDATA%\Python\Python36\Scripts` (on Windows) / `~/.local/bin` (on Linux) to the PATH.

Shortcutter should work on Python 2 or can easily be bugfixed if you post an issue.


# Command line interface

The `-h` or `--help` option will display the help:

```
shortcutter --help
```

```
usage: shortcutter [-h] [-d] [-m] [-n [NAME]] [-s] [-t] [target]

Automatic shortcut creator. Shortcuts auto-activate their environments by 
default.

positional arguments:
  target                The target executable to create Desktop and Menu
                        shortcuts.

optional arguments:
  -h, --help            show this help message and exit
  -d, --desktop         Only create a desktop shortcut.
  -m, --menu            Only create a menu shortcut.
  -n [NAME], --name [NAME]
                        Name of the shortcut without extension (autoname
                        otherwise).
  -s, --simple          Create simple shortcut without activate wrapper.
  -t, --terminal        Create shortcut to environment with shortcutter (plus
                        shortcut to root environment in case of conda).
```


# Python API

[Python API](https://github.com/kiwi0fruit/shortcutter/blob/master/api.rst).


# Operating Systems

Shortcut support Windows, macOS and Linux.

The way shortcuts are provide and applications launched depends on the operating system.

### Windows 

`.lnk` files pointing directly to the application paths are created in the User Desktop and Programs folders.

### macOS

macOS applications are created which run the application via a terminal and copied to the User Desktop (`~/Desktop`) and Launchpad (`/Applications`).

### Linux

`.desktop` files are created which start the application via the shell and created in the User Desktop and applications menu (`~/.local/share/applications`).


# Status

Alpha - tested and works but
[issues](https://github.com/kiwi0fruit/shortcutter/issues) maybe
experienced and API changes are possible.


# Change log

[Change log](https://github.com/kiwi0fruit/shortcutter/blob/master/CHANGE_LOG.md).
