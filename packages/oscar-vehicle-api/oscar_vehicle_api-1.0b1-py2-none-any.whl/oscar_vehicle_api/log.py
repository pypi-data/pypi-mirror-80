#!/usr/bin/env python

###############################################################################
# Copyright 2020 ScPA StarLine Ltd. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import os, sys, time
from logging import basicConfig, warning

import json, uuid
from collections import OrderedDict as odict

basicConfig(format='%(levelname)s:%(message)s')

def error(error_msg):
    sys.exit(error_msg)


class NoIndent(object):
    def __init__(self, value):
        self.value = value


class NoIndentEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        super(NoIndentEncoder, self).__init__(*args, **kwargs)
        self.kwargs = dict(kwargs)
        del self.kwargs['indent']
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, NoIndent):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **self.kwargs)
            return "@@%s@@" % (key,)
        else:
            return super(NoIndentEncoder, self).default(o)

    def encode(self, o):
        result = super(NoIndentEncoder, self).encode(o)
        for k, v in self._replacement_map.iteritems():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result


class VehicleLog():

    def __init__(self, log_dir = "/tmp"):
        self._zero_time = time.time()
        self._id_counter = 0
        self._log_dir = log_dir
        self._data = odict([
            ('header', odict([('ctime', time.strftime("%m.%d.%Y_%H.%M.%S", time.localtime())),
                              ('duration', 0.0),
                              ('size',   0)])),
            ('data', [])
        ])


    def add_data(self, dtime, sw_angle = 0.0,
                              sw_velocity = 0.0,
                              sw_torque = 0.0,
                              eps_torque = 0.0,
                              vehicle_speed = 0.0,
                              mode = 0):

        dtime -= self._zero_time

        self._data['data'].append(NoIndent(odict([('id', self._id_counter),
                                                  ('t', format(dtime, '.4f')),
                                                  ('sw_angle', format(sw_angle, '.1f')),
                                                  ('sw_velocity', format(sw_velocity, '.2f')),
                                                  ('sw_torque', format(sw_torque, '.1f')),
                                                  ('eps_torque', format(eps_torque, '.1f')),
                                                  ('vehicle_speed', format(vehicle_speed, '.2f')),
                                                  ('mode', mode)])))

        self._id_counter += 1


    def _open_file_to_write(self, file_path):

        try:
            file_handler = open(file_path, 'w')
        except Exception as err:
            print("Can't open file " + str(file_path))
            print(err)
            return None

        return file_handler


    def save(self):

        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

        file_path = self._log_dir + "/oscar_vehicle_" + self._data['header']['ctime'] + ".log"

        duration = float(self._data['data'][-1].value['t']) - float(self._data['data'][0].value['t'])
        self._data['header']['duration'] = format(duration, '.4f')

        self._data['header']['size'] = len(self._data['data'])
        file_handler = self._open_file_to_write(file_path)

        if file_handler:
            file_handler.write(json.dumps(self._data, indent=2, cls=NoIndentEncoder))
            file_handler.flush()
            file_handler.close()
            return True
        else:
            return False
