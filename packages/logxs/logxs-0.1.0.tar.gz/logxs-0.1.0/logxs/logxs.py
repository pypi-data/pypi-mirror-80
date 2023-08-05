"""
logx: nice print.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copyright (c) 2020 Min Latt.
License: MIT, see LICENSE for more details.
"""

import logging

class Logxs:
    def __init__(self, ml=False, with_time=False, debug=True):
        self.debug = debug
        _format = "%(asctime)s: %(message)s" if with_time else "%(message)s"
        _level = logging.DEBUG if self.debug else logging.INFO
        logging.basicConfig(format=_format, level=_level, datefmt="%H:%M:%S")
        self.ml = ml
        logging.debug('use `out([any])` method.') if self.debug else logging.info('use `out([any])` method.')
    
    def out(self, *argv):
        self.message = list()
        for arg in argv:
            if self.ml:
                self.message.append(str(arg)+ ' {0}'.format(type(arg)))
            else:
                self.message.append(str(arg))
        for m in self.message:
            logging.debug(m) if self.debug else logging.info(m)



""" this? maybe I previously play with JS -'D """