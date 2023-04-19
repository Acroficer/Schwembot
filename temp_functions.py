from functools import partial
import random

import numpy

def _constant(num):
    return num

def setup_constant(num):
    return partial(_constant, float(num))

def _random(multiplier):
    return random.random() * multiplier

def setup_random(multiplier):
    return partial(_random, float(multiplier))

def _normal(avg, std, absolute, maximum, minimum):
    val = numpy.random.normal(avg, std)
    if absolute: val = avg + abs(val - avg)
    val = max(val, minimum)
    val = min(val, maximum)
    return val

def setup_normal(avg, std, absolute, maximum=2, minimum=0):
    return partial(_normal, float(avg), float(std), absolute.lower() == "true", float(maximum), float(minimum))