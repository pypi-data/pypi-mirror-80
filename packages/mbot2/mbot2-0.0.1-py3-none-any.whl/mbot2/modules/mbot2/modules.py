# -*- coding: utf-8 -*
import struct
from time import ctime, sleep,time
import threading
import mbot2
import mbot2.utils as utils
from mbot2.protocols.PackData import NeuronPackData

class _BaseModule:
    _pack = None
    _is_received = False
    _last_time = 0
    _callback = None
    def __init__(self,board,idx=1,mode=1,period=0):
        self.setup(board,idx,mode,period)

    def quit(self):
        mbot2.quit()

    def setup(self,board,idx,mode=1,period=0):
        board._autoconnect()
        self._board = board
        self._mode = mode
        self._pack = NeuronPackData()
        self._pack.idx = idx
        self._init_module()
    
    def _init_module(self):
        pass

    def force_update(self):
        self._pack.data = [0x1]
        self.request(self._pack)

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)

    def _exist_subscribe(self,subscribe_id):
        return self._board._find_subscribe(subscribe_id)

    def subscribe(self,pack=None):
        pass
    _default_data = [0x7f,NeuronPackData.TYPE_CHANGE,0,0,0,0,0]
    def _subscribe(self,idx,service,subservice,on_response,data=None):
        data = data or self._default_data
        subscribe_id = (idx<<24)+(service<<16)+(subservice<<8)
        if self._exist_subscribe(subscribe_id):
            return subscribe_id
        pack = NeuronPackData()
        pack.on_response = on_response
        pack.idx = idx
        pack.service = service
        pack.subservice = subservice
        pack.data = data
        pack.subscribe_id = subscribe_id
        self._board.request(pack)
        return subscribe_id

    def _run_callback(self,value):
        if not self._callback is None:
            self._callback(value)
        return value

    def _on_parse(self, pack):
        self._pack.data = pack.data
        self._is_received = True

    def read(self,idx,service,subservice,data,callback):
        if not callback is None:
            self._callback = callback
        self._is_received = False
        pack = NeuronPackData()
        pack.subscribe_id = idx
        pack.idx = idx
        pack.service = service
        pack.subservice = subservice
        pack.data = data
        pack.on_response = self._pack.on_response
        self.request(pack)
        if callback is None:
            timeout = 100
            while not self._is_received:
                timeout-=1
                sleep(0.001)
                if timeout<0:
                    break
            return self._pack.data

class Ultrasonic(_BaseModule):
    def _init_module(self):
        self._distance = 0
        self._pack.service = 0x67
        self._pack.subservice = 0x7
        self._pack.on_response = self._on_parse
        self._distance = {}
        
    def _on_parse(self, pack):
        super()._on_parse(pack)
        self._distance[pack.subscribe_id] = super()._run_callback(float('{0:.1f}'.format(utils.bits2float(pack.data[1:6]))))

    def read(self,idx,callback=None):
        res = super().read(idx,self._pack.service,self._pack.subservice,[0x1],callback)
        if idx in self._distance:
            return self._distance[idx]
        return 0.0

    def get_distance(self,idx=0,callback=None):
        idx = idx or self._pack.idx
        return self.read(idx)

class RGBLed(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x67
        self._pack.subservice = 0x7
    
    def set_color(self,index,red,green,blue,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x97,index]
        self._pack.data.extend(utils.ushort2bits(red))
        self._pack.data.extend(utils.ushort2bits(green))
        self._pack.data.extend(utils.ushort2bits(blue))
        self.call(self._pack)
    
class DCMotor(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x67
        self._pack.subservice = 0x7
    
    def set_pwm(self,pwm,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x1]
        self._pack.data.extend(utils.int2bits(pwm))
        self.call(self._pack)


class Car(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x67
        self._pack.subservice = 0x7
    
    def forward(self,speed=50,t=None,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x1]
        self._pack.data.extend(utils.float2bits(speed))
        self._pack.data.extend(utils.long2bits(t))
        self._pack.data.extend(utils.ushort2bits(1))
        self._pack.data.extend(utils.ushort2bits(1))
        self.call(self._pack)
    
    def backward(self,speed=50,t=None,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x2]
        self._pack.data.extend(utils.float2bits(speed))
        self._pack.data.extend(utils.long2bits(t))
        self._pack.data.extend(utils.ushort2bits(1))
        self._pack.data.extend(utils.ushort2bits(1))
        self.call(self._pack)

    def turn_left(self,speed=50,t=None,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x3]
        self._pack.data.extend(utils.float2bits(speed))
        self._pack.data.extend(utils.long2bits(t))
        self._pack.data.extend(utils.ushort2bits(1))
        self._pack.data.extend(utils.ushort2bits(1))
        self.call(self._pack)

    def turn_right(self,speed=50,t=None,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x4]
        self._pack.data.extend(utils.float2bits(speed))
        self._pack.data.extend(utils.long2bits(t))
        self._pack.data.extend(utils.ushort2bits(1))
        self._pack.data.extend(utils.ushort2bits(1))
        self.call(self._pack)

    def stop(self,idx=None):
        self._pack.idx = idx or self._pack.idx
        self._pack.data = [0x9]
        self._pack.data.extend(utils.ushort2bits(1))
        self.call(self._pack)