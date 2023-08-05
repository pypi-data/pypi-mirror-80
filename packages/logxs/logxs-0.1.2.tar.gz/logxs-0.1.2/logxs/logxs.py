"""
logx: nice print.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2020 Min Latt.
License: MIT, see LICENSE for more details.
"""

import logging
class Logxs:
    def __init__(self, ml=False, with_time=False, debug=True, full=True):
        self.with_time = with_time
        self.ml = ml
        self.debug = debug
        self.info = not debug
        self.full = full

        _format = "%(asctime)s: %(message)s" if self.with_time else "%(message)s"
        _level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(format=_format, level=_level, datefmt="%H:%M:%S")
        logging.debug('use `out([any])` method.') if self.debug else logging.info('use `out([any])` method.')
    
    def out(self, *argv):
        self.message = list()
        for arg in argv:
            if self.ml:
                self._check_type(arg) if self.full else self.message.append(str(arg)+ ' {0}'.format(type(arg)))
            else:
                self.message.append(str(arg))

        for m in self.message:
            logging.debug(m) if self.debug else logging.info(m)
        
    def _check_type(self, arg):
        try:
            self.message.append(str(arg)+ ' {0},{1}'.format(type(arg), arg.shape))
        except AttributeError:
            self.message.append(str(arg)+ ' {0}'.format(type(arg)))




""" this? maybe I previously play with JS -'D """