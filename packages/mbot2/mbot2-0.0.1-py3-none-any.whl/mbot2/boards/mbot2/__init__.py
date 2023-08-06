# -*- coding: utf-8 -*

from mbot2.modules.mbot2 import *
from ...boards.base import _BaseBoard
from ...protocols.PackData import NeuronPackData



MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2


def connect(device=None,channel=None):
    return __mbot2(device or channel)

create = connect

class __mbot2(_BaseBoard):
    _device = None
    def __init__(self,device=None):
        self._type = _BaseBoard.Neuron
        if not device is None:
            self._device = device
            super().__init__(_BaseBoard.Neuron,device)
            self.broadcast()

    def broadcast(self):
        self.call(NeuronPackData.broadcast())

    _car = {}
    def Car(self,idx=1):
        if not idx in self._car:
            self._car[idx] = Car(self,idx)
        return self._car[idx]

    @property
    def car(self):
        return self.Car()

    _rgbled = {}
    def RGBLed(self,idx=1):
        if not idx in self._rgbled:
            self._rgbled[idx] = RGBLed(self,idx)
        return self._rgbled[idx]

    @property
    def rgbled(self):
        return self.RGBLed()