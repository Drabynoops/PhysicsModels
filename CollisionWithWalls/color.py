from enum import Enum
import random

class Color:
    BLACK    = (   0,   0,   0)
    WHITE    = ( 255, 255, 255)
    GREEN    = (   0, 255,   0)
    RED      = ( 255,   0,   0)
    BLUE     = (   0,   0, 255)
    GRAY     = ( 127, 127, 127)
    GRAY_2   = (  40,  40,  40)

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))