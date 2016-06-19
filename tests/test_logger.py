import unittest.mock
import time
import os
import sys
import logging
from io import StringIO


# stop auto logger configuration
os.environ['HAPPY_CONSOLE_LOG_LEVEL'] = ''


import happylogging

import tests.a, tests.a.b

#
#def initlog(
#    logger,          # name of logger or logger instance
#    filename=None,   # comma separated list of output file. '-' for stdout
#    rotate=None,     # Log location. 10mb/midnight/1d
#    backups=0,       # Number of backup files
#    encoding=None,   # encoding to open file
#    syslog=None,     # comma separated list of syslog port
#    facility=None    # facility of syslog
#    level=None,      # log level
#    overwrite=True
#):
#

def test_filelog(tmpdir_factory):
    d = tmpdir_factory.mktemp('happylogging')

    filenames = [str(d.join(str(i))) for i in range(3)]
    happylogging.initlog('tests.a', filename=','.join(filenames))
    logging.getLogger('tests.a').warn('hello')

    for f in filenames:
        assert open(f).read().strip().endswith('hello')

def test_stdout():
    stdout = StringIO()
    with unittest.mock.patch('sys.stdout', stdout):
        happylogging.initlog('', filename='-')
        logging.getLogger('').warn('hello')
    assert stdout.getvalue().strip().endswith('hello')

def test_lotate(tmpdir_factory):
    d = (tmpdir_factory.mktemp('happylogging'))
    f = str(d.join('log'))

    happylogging.initlog('tests.a', filename=f, rotate='1mb', backups=10)
    logging.getLogger('tests.a').warn('1'*512*1024)
    logging.getLogger('tests.a').warn('2'*512*1024)
    logging.getLogger('tests.a').warn('3'*512*1024)
    x=open(f).read()
    assert len(x) <  1024*1024

def test_timed(tmpdir_factory):
    d = (tmpdir_factory.mktemp('happylogging'))
    f = str(d.join('log'))

    happylogging.initlog('', filename=f, rotate='04:00', backups=10, propagate=True)
    logging.getLogger('tests.b').warn('1')
    now = time.time()
    with unittest.mock.patch('time.time', return_value=now+24*60*60):
        logging.getLogger('tests.b').warn('2')

    assert open(f).read().strip().endswith('2')


if sys.platform == 'darwin':
    sock = '/var/run/syslog'
else:
    sock = '/var/syslog'

def test_syslog():
    with unittest.mock.patch('logging.handlers.SysLogHandler') as m:
        happylogging.initlog('tests.a', syslog=sock, facility='syslog')
        assert {
            'address': '/var/run/syslog', 
            'facility': 'syslog'
        } == list(m.call_args)[1] 


    happylogging.initlog('tests.a', facility='syslog')
    logging.getLogger('tests.a').warn('333333333333333333333333')
    