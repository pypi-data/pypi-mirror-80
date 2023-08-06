#
# Copyright (c) 2020 eGauge Systems LLC
#       1644 Conestoga St, Suite 2
#       Boulder, CO 80301
#       voice: 720-545-9767
#       email: davidm@egauge.net
#
# All rights reserved.
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
'''This module provides access to the eGauge WebAPI's /api/ctid
service.'''

import os
import secrets
import time

import egauge.ctid
from egauge import webapi

from ..error import Error

def ctid_info_to_table(reply):
    '''Convert a ctid service REPLY to a CTid table.'''
    t = egauge.ctid.Table()
    t.version = reply.get('version')
    t.mfg_id = reply.get('mfgid')
    t.model = reply.get('model')
    t.serial_number = reply.get('sn')
    t.sensor_type = reply.get('k')
    t.r_source = reply.get('rsrc')
    t.r_load = reply.get('rload')

    params = reply.get('params', {})
    t.size = params.get('size')
    t.rated_current = params.get('i')
    t.voltage_at_rated_current = params.get('v')
    t.phase_at_rated_current = params.get('a')
    t.voltage_temp_coeff = params.get('tv')
    t.phase_temp_coeff = params.get('ta')
    t.cal_table = {}
    cal_table = params.get('cal', {})
    for l_str in cal_table:
        l = float(l_str)
        t.cal_table[l] = [cal_table[l_str].get('v', 0),
                          cal_table[l_str].get('a', 0)]
    t.bias_voltage = params.get('bias_voltage')
    t.scale = params.get('scale')
    t.offset = params.get('offset')
    t.delay = params.get('delay')
    t.threshold = params.get('threshold')
    t.hysteresis = params.get('hysteresis')
    t.debouce_time = params.get('debounce_time')
    t.edge_mask = params.get('edge_mask')
    t.ntc_a = params.get('ntc_a')
    t.ntc_b = params.get('ntc_b')
    t.ntc_c = params.get('ntc_c')
    t.ntc_m = params.get('ntc_m')
    t.ntc_n = params.get('ntc_n')
    t.ntc_k = params.get('ntc_k')
    return t

class CTidInfoError(Error):
    '''Raised if for any CTid info related errors.'''

class PortInfo:
    '''Encapsulates the port number on which a CTid table was read, the
    polarity which is was read with, and the table itself.

    '''
    def __init__(self, port, polarity, table):
        self.port = port
        self.polarity = polarity
        self.table = table

    def port_name(self):
        '''Return the canonical port name.'''
        return 'S%d' % self.port

    def short_mfg_name(self):
        '''Return the short (concise) name of the manufacturer of the sensor
        or `-' if unknown.

        '''
        if self.table is None or self.table.mfg_id is None:
            return '-'
        return egauge.ctid.mfg_short_name(self.table.mfg_id)

    def model_name(self):
        '''Return the model name of the sensor attached to the port.  If
        unknown `-' is returned.

        '''
        if self.table is None or self.table.model is None:
            return '-'
        return self.table.model

    def mfg_model_name(self):
        '''Return a "fully qualified" model name, which consists of the short
        version of the manufacter's name, a dash, and the model
        name.

        '''
        return '%s-%s' % (self.short_mfg_name(), self.model_name())

    def sn(self):
        '''Return the serial number or None if unknown.'''
        if self.table is None or self.table.serial_number is None:
            return None
        return self.table.serial_number

    def serial_number(self):
        '''Return the serial number of the sensor attached to the port as a
        decimal string.  If unknown, '-' is returned.

        '''
        if self.table is None or self.table.serial_number is None:
            return '-'
        return str(self.table.serial_number)

    def unique_name(self):
        '''Return a sensor's unique name, which is a string consisting of the
        manufacturer's short name, the model name, and the serial
        number, all separated by dashes..

        '''
        return '%s-%s' % (self.mfg_model_name(), self.serial_number())

    def sensor_type(self):
        '''Return the sensor type of the sensor attached to the port or None
        if unknown.

        '''
        if self.table is None or self.table.sensor_type is None:
            return None
        return self.table.sensor_type

    def sensor_type_name(self):
        '''Return the name of the sensor type of the sensor attached to the
        port or '-' if unknown.

        '''
        st = self.sensor_type()
        if st is None:
            return '-'
        return egauge.ctid.get_sensor_type_name(st)

    def __str__(self):
        return '(port=%d,polarity=%s,table=%s)' % (self.port, self.polarity,
                                                   self.table)

class CTidInfo:
    def __init__(self, dev):
        '''Create an object which can be used to access the CTid service of
        device DEV.  The service allows reading CTid info from a
        particular port, scan for such info, flash the attached
        sensor's indicator LED, or iterate over all the ports with
        CTid information.

        '''
        self.dev = dev
        self.tid = None
        self.info = None
        self.index = None

    def _make_tid(self):
        '''Create a random transaction ID.'''
        self.tid = secrets.randbits(32)
        if self.tid < 1:
            self.tid += 1

    def stop(self):
        '''Stop pending CTid operation, if any.'''
        if self.tid is not None:
            self.dev.post('/ctid/stop', {})
        self.tid = None

    def scan(self, port_number):
        '''Scan the CTid information from the sensor attached to the specified
        PORT_NUMBER and return A PortInfo object as a result.  If no
        CTid info could be read from the port, the returned object's
        table member will be None.

        '''
        if self.tid is not None:
            self.stop()

        for polarity in ['+', '-']:
            self._make_tid()
            data = {'op': 'scan', 'tid': self.tid, 'polarity': polarity}
            resource = '/ctid/%d' % port_number
            for _ in range(3):
                try:
                    reply = self.dev.post(resource, data)
                    if reply.get('status') == 'OK':
                        break
                except Error:
                    pass
            for _ in range(20):
                time.sleep(.25)
                reply = self.dev.get(resource, params={'tid': self.tid})
                if reply.get('port') == port_number:
                    if reply.get('tid') == self.tid:
                        return PortInfo(port_number, polarity,
                                        ctid_info_to_table(reply))
                    break
            self.stop()
        return PortInfo(port_number, None, None)

    def flash(self, port_number, polarity='-'):
        '''Flash the indicator LED on the sensor attached to the specified
        PORT_NUMBER using the specified POLARITY.  Flashing will
        continue until stop() is called (or until a timeout occurs
        after about 30 minutes).

        '''
        if self.tid is not None:
            self.stop()
        self._make_tid()
        data = {'op': 'scan', 'tid': self.tid, 'polarity': polarity}
        resource = '/ctid/%d' % port_number
        for _ in range(3):
            try:
                reply = self.dev.post(resource, data)
                if reply.get('status') == 'OK':
                    break
            except Error:
                pass

    def delete(self, port_number):
        '''Delete the CTid information stored for the specified port
        number.

        '''
        resource = '/ctid/%d' % port_number
        reply = self.dev.delete(resource)
        if reply is None or reply.get('status') != 'OK':
            raise CTidInfoError('Failed to delete CTid info.', port_number)

    def get(self, port_number):
        '''Get the CTid information stored for the specified PORT_NUMBER (if
        any).

        '''
        resource = '/ctid/%d' % port_number
        reply = self.dev.get(resource)
        if reply is None:
            raise CTidInfoError('Failed to read CTid info.', port_number)
        if len(reply) == 0:
            return None
        if reply.get('port') != port_number:
            raise CTidInfoError('CTid info has incorrect port number.',
                                reply.get('port'), port_number)
        return PortInfo(port_number, reply.get('polarity'),
                        ctid_info_to_table(reply))

    def __iter__(self):
        '''Iterate over all available CTid information.'''
        reply = self.dev.get('/ctid')
        self.info = reply.get('info', [])
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.info):
            raise StopIteration
        info = self.info[self.index]
        t = ctid_info_to_table(info)
        self.index += 1
        return PortInfo(info['port'], info['polarity'], t)

if __name__ == '__main__':
    from . import device
    dut = os.getenv('EGAUGE_DUT')
    usr = os.getenv('EGAUGE_USR')
    pwd = os.getenv('EGAUGE_PWD')
    ctid_info = CTidInfo(device.Device(dut, auth=webapi.JWTAuth(usr, pwd)))
    print('SCANNING')
    port_info = ctid_info.scan(port_number=3)
    print('  port_info[%d]' % port_info.port, port_info.table)
    print('-'*40)
    print('ITERATING')
    for t in ctid_info:
        print('  port %d%s:' % (t.port, t.polarity), t.table)

    print('DELETING')
    ctid_info.delete(port_number=3)
    port_info = ctid_info.get(port_number=3)
    if port_info is None:
        print('  no CTid info for port 3')
    else:
        print('  port_info[%d]' % port_info.port, port_info.table)

    print('FLASHING')
    ctid_info.flash(port_number=3)
    time.sleep(5)
    ctid_info.stop()
