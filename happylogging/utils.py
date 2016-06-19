import logging
import cProfile
import functools
import threading
import pprint

logdata = threading.local()
INDENT_WIDTH = 2
MAX_INDENT = 20

COLORS = {
    "RED": '\033[91m',
    "GREEN":  '\033[92m',
    "YELLOW":  '\033[93m',
    "BLUE":  '\033[94m',
    "MAGENTA":  '\033[95m',
    "CYAN":  '\033[96m',
    "RESET":  '\033[0m',
}

def _getLocal(name):
    if not hasattr(logdata, name):
        setattr(logdata, name, {})
    return getattr(logdata, name)

def inject_logger_wrapper(ns, name):
    org = getattr(ns, name)

    def _get_indent():
        d = _getLocal('indent')
        return d.setdefault(name.upper(), 0)

    def _add_indent(n):
        d = _getLocal('indent')
        d[name.upper()] = min(max(0, _get_indent() + n), MAX_INDENT)

    @functools.wraps(org)
    def f(self, msg, *args, **kwargs):
        indent = _get_indent()

        return org(self, ' '*indent + msg, *args, **kwargs)

    setattr(ns, name, f)

    # utifily functions
    def begin_block():
        _add_indent(INDENT_WIDTH)

    def end_block():
        _add_indent(-1*INDENT_WIDTH)

    def setcolor(color=None):
        if color:
            color = COLORS[color]
        d = _getLocal('color')
        d[name.upper()] = color

    g = getattr(logging, name)
    f.block = g.block = begin_block
    f.endblock = g.endblock = end_block
    f.setcolor = g.setcolor = setcolor

inject_logger_wrapper(logging.Logger, 'debug')


def inject_streamhandler_wrapper():
    org_format = logging.StreamHandler.format

    def get_color(levelname):
        d = _getLocal('color')
        return d.setdefault(levelname, None)

    @functools.wraps(org_format)
    def format(self, record):
        ret = org_format(self, record)
        if self.stream.isatty():
            color = get_color(record.levelname.upper())
            if color:
                ret = color+ret+'\033[0m'
        return ret
    logging.StreamHandler.format = format

inject_streamhandler_wrapper()
