============================
happylogging
============================

Utility functions to help using standard logging module.


Requirements
============

* Python 3.4 or later


Configure logging
=========================


initlog()
----------------

``initlog(logger=None, overwrite=True, level=None, format=DEFAULT_FORMAT, propagate=False, filename=None, rotate=None, backups=0, encoding=None, syslog=None, facility=None)``


``initlogin()`` configures various logging in a function.

``logger`` is a name of logger or logger instance to configure. If ``logger`` is None or empty string, Root logger is configured. 

Logging configuration is overwritten if ``overwrite`` is ``True``. To add handler to the logger instead of replace, ``overwrite`` should be ``False``. 

``level`` should be an one of ``'CRITICAL'``, ``'WARNING'``, ``'INFO'``, ``'DEBUG'``.


Configure to logging to files
+++++++++++++++++++++++++++++++++++++

``filename`` is a comma separated list of file names to emit logs. To print to a stdout, specify ``-`` as filename.

::

   import happylogging
   initlog(filename='log.log, -', level='DEBUG')   # Logging to log.log and stdout


``rotate`` specifies how to log files rotated. 

- rotate by size

  You can specify size to rotates file such as ``100mb`` or ``2gb``.

::

    initlog(filename='log.log', rotate='10mb')   # Rotate files every 10 MB.

- rotate by time.

  You can specify when to rotate files. Valid values are conbination of interval value and type.

  - Digits followed by ``'S'`` specify to rotate every n seconds. e.g. ``100S`` rotates in every 100 seconds. Similary, ``'M'``, ``"H"`` and ``"D"`` specify Minutes, Hours and Days respecivly.

  - To rotate every day, you can specify time to rotate such as ``02:00``.

::

    initlog(filename='log.log', rotate='10D')   # Rotate files in every 10 Days
    initlog(filename='log.log', rotate='04:30')   # Rotate files at 04:30 every day

- If rotate specified, you can also specify number of backups of log file to ``backups`` arg.

::

    initlog(filename='log.log', rotate='10D', backups=10)   # Retain 10 back ups

- ``encoding`` specifies encoding of log file.


Configure to logging to syslog
+++++++++++++++++++++++++++++++++++++


To logging to syslog server, you can use ``syslog`` to specify syslog servers as commna separated list of servers. Each servers are apecified as ``HOST:PORT`` form or ``/path/to/udp/port`` form. If ``syslog`` is omitted, ``localhost:514`` is assumed. To logging to syslog, ``facility`` must not be omitted.


::

    initlog(syslog='/var/syslog, example:514', facility='syslog')   # Send to local port and host 'example'

::

    initlog(filename='-', facility='syslog')  # Send to stdout and local syslog server.



Utility functions
========================

After ``happylogging`` was imported, logging methods such as ``logging.info()`` gains some addtional methods.

block()/encblock()
--------------------

Define indented block of logs.

::

   >>> import logging, happylogging
   >>> happylogging.initlog(filename='log.log', level='DEBUG')
   >>> logging.debug('first line')
   >>> logging.debug.block()
   >>> logging.debug('indented!')
   >>> logging.debug.block()
   >>> logging.debug('more indented!')
   >>> logging.debug.endblock()
   >>> logging.debug.endblock()
   >>> logging.debug('no more!')
   >>> print(open('log.log').read())
   2016-06-19 14:50:01,121 DEBUG first line
   2016-06-19 14:50:24,225 DEBUG   indented!
   2016-06-19 14:50:35,806 DEBUG     more indented!
   2016-06-19 14:50:56,835 DEBUG no more!

Indent is defined per thread and logging level (CRITICAL, WARNING, ...).

setcolor(color=None)
----------------------

Change color of log if log is directed to the tty. ``color`` should be one of string 
``"RED"``, ``"GREEN"``, ``"YELLOW"``, ``"BLUE"``, ``"MAGENTA"``,``"CYAN"``.

To reset color, specify ``None`` as color.

``setcolor()`` doesn't work if output device is file or syslogs.

::

   >>> happylogging.initlog(filename='-', level='DEBUG')  # log to console
   >>> logging.debug.setcolor("RED")   # Change text color of debug to red.
   >>> logging.debug.setcolor(None)    # Restore color


Copyright 
=========================

Copyright (c) 2016 Atsuo Ishimoto

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
