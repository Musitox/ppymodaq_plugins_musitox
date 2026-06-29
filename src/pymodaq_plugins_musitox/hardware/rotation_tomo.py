#this is part of pymodaq test for Musitox project
#it deals with simulating a rotation actuator for tomography

#Author : Pierre Piault for 3SR -- Grenoble // CNRS laboratory

import numpy as np

from pymodaq.utils.math_utils import gauss1D
from typing import List, Union
from collections.abc import Iterable
from numbers import Number
import math
from time import perf_counter

class Rotation_tomo:
    """Mock Controller of a tomographic rotation
    it should contain absolute, relative mouvment
    setting of 0deg or home position
    """

    infos = 'Tomographic rotation Wrapper 0.1.0'

    def __init__(self):
        super().__init__()


        self._epsilon = 0.01 #margin of position error
        #self._tau = 2   #time to reach the position
        self._moving = False

    def open_communication(self):
        #connect the device
        return True

    def close_communication(self):
        #disconnect the device
        return False

    def stop(self):
        #stop the motion
        self._moving = False

    @tau.setter
    def tau(self, value):
        """
        Set the characteristic time to reach a particular rotation angular position
        Parameters
        ----------
        value: (float) a strictly positive characteristic time in seconds
        """
        if value <= 0:
            raise ValueError(f'A characteristic time of {value} is not possible. It should be strictly positive')
        else:
            self._tau = value

            
