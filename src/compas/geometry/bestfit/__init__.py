from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas

from .bestfit import *

if not compas.IPY:
    from .bestfit_numpy import *


__all__ = [name for name in dir() if not name.startswith('_')]
