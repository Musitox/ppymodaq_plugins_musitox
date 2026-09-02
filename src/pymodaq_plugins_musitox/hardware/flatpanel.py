# -*- coding: utf-8 -*-
"""
Created the 26/08/2026

@author: Pierre Piault
"""
import numpy as np
from skimage.data import shepp_logan_phantom
from skimage.transform import radon, rescale

import pymodaq_utils.math_utils as mutils


class Mock_flatpanel:


    Nx = 240
    Ny = 240
    amp = 20
    #dx = 20
    #dy = 40
    #n = 1
    expT = 10
    amp_noise = 4

    theta = 0
    axes = ['bin1', 'bin2', 'bin3']
    units = ['pxls', 'pxls', 'pxls']

    hardware_averaging = True
    live_mode_available = True

    def __init__(self):
        super().__init__()
        self._image = None
        #self._current_value = dict(expT = 10, theta=0.)
        self.base_Mock_data()
        self._axes = self.axes[0]

    def open_communication(self):
        # connect the device
        return True

    def close_communication(self):
        # disconnect the device
        return True

    def get_value(self, axis):
        #get value from the device to the gui pymodaq
        return self._current_value[axis]

    def set_value(self, axis, value):
        #set the value from the gui pymodaq toward the device
        self._current_value[axis] = value
        #then actualisation of the image
        self.base_Mock_data()


    def base_Mock_data(self):
        # build the base of the image
        #this should be adapted with the selected binning
        self.x_axis = np.linspace(0, self.Nx, self.Nx, endpoint=False) - self.Nx/2
        self.y_axis = np.linspace(0, self.Ny, self.Ny, endpoint=False) - self.Ny/2
        # then it fill with a image
        self._image = self.make_Mock_data()
        return self._image

    def make_Mock_data(self):
        # make the mock image of tomography
        # this should be adapted by the exposure time and binning
        theta = self.theta
        sample_slice = rescale(shepp_logan_phantom(), scale=0.6, mode='reflect', channel_axis=None)
        radio = radon(sample_slice, theta=[theta])
        radio = np.tile(radio,(1,self.Nx))
        '''
        sample = np.tile(sample_slice[:,:,np.newaxis], (1,1,self.Nx))
        radio = np.zeros((self.Nx, self.Nx))
        for i in range(sample.shape[2]):
            radio[i,:] = radon(sample[:,:,i], theta=theta)
        '''
        return radio

    def get_data(self) -> np.ndarray:
        # build a realistic image with random noise
        return self.amp * self.expT * self.make_Mock_data() + self.amp_noise * np.random.rand(len(self.y_axis), len(self.x_axis))