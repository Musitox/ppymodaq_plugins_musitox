# -*- coding: utf-8 -*-
"""
Created the 26/08/2026

@author: Pierre Piault
"""
import numpy as np
import pymodaq_utils.math_utils as mutils


class mock_flatpanel:
    Nx = 256
    Ny = 256
    amp = 20
    dx = 20
    dy = 40
    n = 1
    is_drifting = False
    drift_x = 0
    drift_y = 0
    drift = np.zeros(2)
    std_x = 0
    std_y = 0
    amp_noise = 4
    fringes = False
    axes = ['exp', 'Rot']
    units = ['ms', '°']

    def __init__(self):
        super().__init__()
        self._image: np.ndarray = None
        self._current_value = dict(exp = 1., Rot=0.)
        self.base_Mock_data()
        self.refresh_drift()

    def refresh_drift(self):
        #???? je ne sais pas ce que c'est
        self.drift = np.zeros(2)

    def get_value(self, axis: str):
        ## doit etre le retour de valeur de la valeur existante dans axes = [...
        return self._current_value[axis]

    def set_value(self, axis: str = 'exp', value: float = 0.):
        #set exposuer time
        self._current_value[axis] = value
        self.base_Mock_data()

    def base_Mock_data(self):
        self.x_axis = np.linspace(0, self.Nx, self.Nx, endpoint=False) - self.Nx / 2
        self.y_axis = np.linspace(0, self.Ny, self.Ny, endpoint=False) - self.Ny / 2
        self._image = self.make_Mock_data()
        return self._image

    def make_Mock_data(self):
        if self.is_drifting:
            self.drift[0] += self.drift_x + self.std_x * np.random.randn()
            self.drift[1] += self.drift_y + self.std_y * np.random.randn()
        data_mock = self.amp * (
            mutils.gauss2D(self.x_axis, self._current_value['X'] - self.drift[0], self.dx,
                           self.y_axis, self._current_value['Y'] - self.drift[1], self.dy,
                           self.n,
                           angle=self._current_value['Theta']))
        if self.fringes:
            for indy in range(data_mock.shape[0]):
                data_mock[indy, :] = data_mock[indy, :] * np.sin((self.x_axis - self.drift[0]) / 4) ** 2
        return data_mock

    def get_data(self) -> np.ndarray:
        return self.make_Mock_data() + self.amp_noise * np.random.rand(len(self.y_axis), len(self.x_axis))