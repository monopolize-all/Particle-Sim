import sys, os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from preferences import *


from particles.solid import Solid


class Fluid(Solid):

    BASE_COLOUR = (0, 117, 119)
