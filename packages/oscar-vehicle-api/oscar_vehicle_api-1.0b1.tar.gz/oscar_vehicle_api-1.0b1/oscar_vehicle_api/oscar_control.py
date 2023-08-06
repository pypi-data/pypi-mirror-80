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

import inspect
import sys
import log
import threading

def available_controllers():

    controllers = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            controllers.update({name: obj})

    return controllers


def create_controller_by_name(name, params = None):

    if name:
        controllers = available_controllers()
        if name in controllers:
            return controllers[name](params)
        else:
            log.warning("There is no " + str(interface) + " controller!")

    return None


class BaseController(object):

    def __init__(self, params = None):
        self._params = {}

        self.state_lock = threading.Lock()

        self._target_vehicle_speed        = None
        self._target_vehicle_acceleration = None
        self._target_vehicle_jerk         = None

        self._target_steering_angle          = None
        self._target_steering_angle_velocity = None

        self._current_vehicle_speed        = None
        self._current_vehicle_acceleration = None
        self._current_vehicle_jerk         = None

        self._current_vehicle_speed_receive_time        = 0.0
        self._current_vehicle_acceleration_receive_time = 0.0
        self._current_vehicle_jerk_receive_time         = 0.0

        self._current_steering_angle          = None
        self._current_steering_angle_velocity = None

        self._current_steering_angle_receive_time           = 0.0
        self._current_steering_angle_velocity_receive_time  = 0.0

        self._output_vehicle_throttle = None
        self._output_steering_torque      = None


    def update_params(self, params):
        self._params.update(params)


    def get_params(self):
        return self._params


    def reset():
        pass


    def set_current_vehicle_speed(self, vehicle_speed, receive_time = None):
        self._current_vehicle_speed = vehicle_speed
        if receive_time:
            self._current_vehicle_speed_receive_time = receive_time


    def set_current_vehicle_acceleration(self, vehicle_acceleration, receive_time = None):
        self._current_vehicle_acceleration = vehicle_acceleration
        if receive_time:
            self._current_vehicle_acceleration_receive_time = receive_time


    def set_current_steering_wheel_angle(self, steering_wheel_angle, receive_time = None):
        self._current_steering_angle = steering_angle
        if receive_time:
            self._current_steering_angle_receive_time = receive_time


    def set_current_steering_wheel_velocity(self, steering_wheel_velocity, receive_time = None):
        self._current_steering_angle_velocity = steering_angle_velocity
        if receive_time:
            self._current_steering_angle_velocity_receive_time = receive_time


    def set_target_speed(self, speed = None, acceleration = None, jerk = None):
        self._target_vehicle_speed        = speed
        self._target_vehicle_acceleration = acceleration
        self._target_vehicle_jerk         = jerk


    def set_target_steering(self, steering_angle = None, steering_angle_velocity = None):
        self._target_steering_angle          = steering_angle
        self._target_steering_angle_velocity = steering_angle_velocity


    def calc_output():
        return self._output_vehicle_throttle, self._output_steering_torque


class Test(BaseController):

    def __init__(self,  *args, **kwargs):
        super(BaseController, self).__init__(*args, **kwargs)

        self._params = {"P": 0.1,
                        "I": 0.1,
                        "D": 0.01}
