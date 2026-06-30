#this is part of pymodaq test for Musitox project
#it deals with simulating a rotation actuator for tomography

#Author : Pierre Piault for 3SR -- Grenoble // CNRS laboratory



from pymodaq.utils.math_utils import gauss1D
from typing import List, Union
from collections.abc import Iterable
from numbers import Number
import math
import numpy as np
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
        self._position = 10

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


    def set_position(self, value, set_type='abs'):
        """Move the rotation to the position
        set_type should be 'abs' if absolute mouvment
        or not 'abs' it is relative mouvment
        """

        if set_type == 'abs' and value < 0:
            raise ValueError('current mock rotation cannot be negative')
        if set_type == 'abs':
            self._target_pos = value
        else:
            self._target_pos = self._position + value

        self._init_value = self._position
        if self._init_value != self._target_pos:
            self._alpha = math.fabs(math.log(self._espilon / math.fabs(self._init_value - self._target_pos)))
        else:
            self._alpha = math.fabs(math.log(self._espilon / 10))
        self._start_time = perf_counter()
        self._moving = True

        def get_position(self):
            """get the current position of the rotation actuator"""
            return self._position

        @property
        def data_position(self, ):
            return self._pos0


        @data_position.setter
        def data_position(self, pos0):
            """Defines the center wavelength of the spectrum peak to be measured"""
            if pos0 < 0:
                raise ValueError('current mock rotation cannot be negative')
            self._pos0 = pos0
            
