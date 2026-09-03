import numpy as np
from qtpy.QtCore import QThread, Slot, QRectF
from qtpy import QtWidgets

from typing import Union, List, Dict
from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

#  TODO:
#  Replace the following fake import with the import of the real Python wrapper of your instrument. Here we suppose that
#  the wrapper is in the hardware directory, but it could come from an external librairy like pylablib or pymeasure.
from pymodaq_plugins_musitox.hardware.flatpanel import Mock_flatpanel


# TODO:
# (1) change the name of the following class to DAQ_2DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_2Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_2D


class DAQ_2DViewer_Flatpanel(DAQ_Viewer_base):
    """ Instrument plugin class for a 2D viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any
    """
    is_multiaxes = True
    _axis_names: Union[list[str], Dict[str, int]] = ['Bin x1', 'Bin x2', 'Bin x3']
    _controller_units: Union[str, List[str]] = ['pxls', 'pxls', 'pxls']
    _epsilon: Union[float, List[float]] = 0.1
    #data_actuator_type = DataActuatorType.DataActuator

    params = comon_parameters + [
        {'title':'Exposure time (ms)', 'name':'expTime', 'type':'int', 'value':'100', 'default':100, 'min':0, 'max':1000, 'readonly':False},
        {'title':'rotation (°)', 'name':'rot', 'type':'float', 'value':0,'default':0, 'min':0., 'max':180., 'readonly':False},
        #{'title':'Binning', 'name':'binning', 'type':'int', 'value':1, 'default':1, 'min':1, 'max':3}
        ## TODO for your custom plugin
        # elements to be added here as dicts in order to control your custom stage
        ############
    ]

    def ini_attributes(self):
        #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        #  autocompletion
        self.controller: Mock_flatpanel = None

        self.live = False
        #self.x_axis = None
        #self.y_axis = None

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        # TODO for your custom plugin
        #the thing to do for exposure time
        if param.name() == 'axis':
            #this is the binning case
            self.controller.your_method_to_apply_this_param_change()
        elif param.name() == 'expTime':
            self.controller.set_value('expTime', param.value())
        elif param.name() == 'rot':
            self.controller.set_value('rot', param.value())

        else :
            pass

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        #raise NotImplementedError  # TODO when writing your own plugin remove this line and modify the one below

        if self.is_master:
            self.controller = Mock_flatpanel()  #instantiate you driver with whatever arguments are needed
            #self.controller.open_communication() # call eventual methods
            initialized = self.controller.open_communication()  # TODO
        else:
            self.controller = Mock_flatpanel()
            initialized = True

        self.x_axis = Axis(data=self.controller.x_axis, label='pixel', index=1)
        self.y_axis = Axis(data=self.controller.y_axis, label='pixel', index=0)

        '''
        ## TODO for your custom plugin
        # get the x_axis (you may want to to this also in the commit settings if x_axis may have changed
        data_x_axis = self.controller.your_method_to_get_the_x_axis()  # if possible
        self.x_axis = Axis(data=data_x_axis, label='', units='', index=1)

        # get the y_axis (you may want to to this also in the commit settings if y_axis may have changed
        data_y_axis = self.controller.your_method_to_get_the_y_axis()  # if possible
        self.y_axis = Axis(data=data_y_axis, label='', units='', index=0)

        ## TODO for your custom plugin. Initialize viewers pannel with the future type of data
        self.dte_signal_temp.emit(DataToExport('myplugin',
                                               data=[DataFromPlugins(name='Mock1', data=["2D numpy array"],
                                                                     dim='Data2D', labels=['dat0'],
                                                                     axes=[self.x_axis, self.y_axis]), ]))
        '''
        info = "Detector initialized"
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        #raise NotImplementedError  # when writing your own plugin remove this line
        if self.is_master:
            self.controller.close_communication()

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following
        #self.x_axis = np.linspace(0, self.Nx, self.Nx, endpoint=False)
        #self.y_axis = np.linspace(0, self.Ny, self.Ny, endpoint=False)

        if 'live' in kwargs:
            if kwargs['live']:
                self.live = True
                # self.live = False  # don't want to use that for the moment

        if self.live:
            while self.live:
                #data = self.average_data(Naverage)  # hardware averaging
                myradio = self.controller.get_data()
                data = DataFromPlugins(name='myXradio', data=[myradio])
                #data = DataFromPlugins(name='myXradio', data=[myradio], axes=[self.x_axis, self.y_axis])
                QThread.msleep(kwargs.get('wait_time', 100))
                self.dte_signal.emit(DataToExport('myXradio', data=[data]))
                QtWidgets.QApplication.processEvents()
        else:
            myradio = self.controller.get_data()
            data = DataFromPlugins(name='myXradio', data=[myradio], axes=[self.x_axis, self.y_axis])
            QThread.msleep(000)
            self.dte_signal.emit(DataToExport('myXradio', data=[data]))

        # #dte = self.average_data(Naverage)
        # data_tot = self.controller.get_data()
        # '''
        # self.dte_signal.emit(DataToExport('myXradio',
        #                                   data=[DataFromPlugins(name='Mock_flatpanel', data=[data_tot],
        #                                                         dim='Data2D', labels=['label1'],
        #                                                         axes=[self.x_axis, self.y_axis]), ]))
        # '''
        # dte = DataFromPlugins('myXradio',data=[data_tot],axes=[self.x_axis,self.y_axis] )
        #
        # self.det_signal.emit(DataToExport('myXradio', data=[dte]))
        # ##asynchrone version (non-blocking function with callback)
        # #self.controller.your_method_to_start_a_grab_snap(self.callback)
        # #########################################################

    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport('myplugin',
                                          data=[DataFromPlugins(name='Mock_flatpanel', data=[data_tot],
                                                                dim='Data2D', labels=['label1'],
                                                                x_axis=self.x_axis,
                                                                y_axis=self.y_axis), ]))
    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        ## TODO for your custom plugin
        #raise NotImplementedError  # when writing your own plugin remove this line
        #self.controller.your_method_to_stop_acquisition()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        ##############################
        self.live = False
        return ''


if __name__ == '__main__':
    main(__file__)
