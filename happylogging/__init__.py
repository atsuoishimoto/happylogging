import os
import sys
import re
import datetime
import logging, logging.handlers
from . import utils

#level=debug
#stream=stdout, stderr
#file= ./abc, ./def  # comma separated list of output file
#encoding=utf8
#rotate=10mb midnight 1d
#syslog=localhost:514, /dev/log
#facility=syslog
#format=

#def setlevel(level)
#
#def fileconfig(level, filename, encoding, rotate):
#
#def streamconfig(level, stream);
#
#def syslogconfig(level, syslog, facility):
#
#def condig(listOfDict)
#

default_time = datetime.time(4, 0)

def deleteHandlers(logger):
    with logging._lock:
        logger.handlers[:] = []


def set_logger(logger, handler, level, overwrite):
    if overwrite:        deleteHandlers(logger)
    logger.addHandler(handler)

    if level is not None:
        logger.setLevel(level)


def build_file_handler(filename, encoding=None, rotate=None, 
                    backups=1, at=default_time):
    if rotate:
        kargs = {}
        m = re.match(r'(\d+)(m|g)b', rotate)
        if m:
            size, order = m.groups()
            maxBytes = int(size)*1024**2*((1024 if order == 'g' else 1))
            if not maxBytes:
                raise ValueError('Invalid maxBytes: '+rotate)

            handler = logging.handlers.RotatingFileHandler(
                filename, encoding=encoding, maxBytes=maxBytes,
                backupCount=backups)
        else:
            # S - Seconds
            # M - Minutes
            # H - Hours
            # D - Days
            # 00:00 - roll over at midnight
            # W{0-6} - roll over on a certain day; 0 - Monday
            m = re.match(r'(\d+)(S|M|D)|(\d\d:\d\d)|(W\d)', rotate)
            if not m:
                raise ValueError('Invalid rotate specifier: '+rotate)
            
            interval = int(m.group(1) or 0)
            if interval:
                when = m.group(2)
            else:
                s = m.group(3)
                if s:
                    when = 'midnight'
                    h, m = s.split(':')
                    at = datetime.time(int(h), int(m))
                else:
                    when = m.group(0)

            handler = logging.handlers.TimedRotatingFileHandler(
                filename, encoding=encoding, when=when, interval=interval, 
                atTime=at)

    else:
        handler = logging.FileHandler(filename, encoding=encoding)
    return handler


DEFAULT_FORMAT = '%(asctime)s %(levelname)s %(message)s'

def initlog(
    logger=None,     # name of logger or logger instance
    overwrite=True,  # remove existing handlers of the logger
    propagate=False, #
    format=DEFAULT_FORMAT,
    level=None,      # log level
    filename=None,   # comma separated list of output file. '-' for stdout
    rotate=None,     # Log location. 10mb/midnight/1d
    backups=0,       # Number of backup files
    encoding=None,   # encoding to open file
    syslog=None,     # comma separated list of syslog port
    facility=None,   # facility of syslog
):

#encoding=utf8
#rotate=10mb 04:00 1d
#syslog=localhost:514, /dev/log
#facility=syslog
#format=
    if isinstance(logger, (str, type(None))):
        logger = logging.getLogger(logger)

    if level:
        logger.setLevel(level)

    if propagate is not None:
        logger.propagate = propagate

    if overwrite:
        deleteHandlers(logger)
    
    formatter = logging.Formatter(format)
    
    if filename:
        filenames = [f.strip() for f in filename.split(',')]
    
        for f in filenames:
            if f == '-':
                handler = logging.StreamHandler(sys.stdout)
                handler.setFormatter(formatter)
            else:
                handler = build_file_handler(f, encoding=encoding, rotate=rotate, 
                        backups=backups, at=default_time)
                handler.setFormatter(formatter)

            logger.addHandler(handler)

    if facility:
        ports = []
        syslog = syslog or 'localhost:514'
        ports = [s.strip() for s in syslog.split(',')]
        for p in ports:
            if ':' in p:
                host, port = p.split(':')
                p = (host, int(port))

            handler = logging.handlers.SysLogHandler(address=p, facility=facility)
            handler.setFormatter(formatter)

            logger.addHandler(handler)


HAPPY_ENV_VAR = 'HAPPY_CONSOLE_LOG_LEVEL'
def configureDefaultLogger():
    if not sys.stdout.isatty():
        return
    loglv = os.environ.get('HAPPY_CONSOLE_LOG_LEVEL')
    if loglv:
        initlog('', overwrite=False, filename='-', level=loglv)

configureDefaultLogger()



