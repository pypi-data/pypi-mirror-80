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

import threading
import time

from math import cos, sin, tan

import oscar_protocol
from loops import Spinner
from slp import print_raw
from oscar_control import *
from oscar_vehicle_interfaces import create_interface_by_name

import log

OSCAR_DEFAULT_CONTROL_RATE = 50
OSCAR_DEFAULT_ODOMETRY_CALC_RATE = 50
OSCAR_DEFAULT_LOG_RATE = 50
OSCAR_DEFAULT_LOG_DIR  = "/tmp/oscar_vehicle_api_logs"


class OscarVehicle(object):

    UNKNOWN                   = oscar_protocol.UNKNOWN
    VEHICLE_AUTO_MODE         = oscar_protocol.VEHICLE_AUTO_MODE
    VEHICLE_MANUAL_MODE       = oscar_protocol.VEHICLE_MANUAL_MODE

    def __init__(self, interface          = None,
                       protocol_config    = None,
                       controller         = None,
                       controller_params  = None,
                       control_loop_rate  = OSCAR_DEFAULT_CONTROL_RATE,
                       odometry_loop_rate = OSCAR_DEFAULT_ODOMETRY_CALC_RATE):

        self._vehicle_protocol  = oscar_protocol.OscarProtocol(protocol_config)
        self._vehicle_interface = create_interface_by_name(interface, self._vehicle_protocol)

        if self._vehicle_interface:
            self._vehicle_interface.start_communication()

        self.vehicle_params = {"wheel_radius":             0.37,
                               "wheel_width":              0.25,
                               "wheelbase":                2.75,
                               "axle_track":               1.64,
                               "steering_ratio":           14.8,
                               "max_steering_wheel_angle": 500,  # ~ 33.78 deg
                               "max_acceleration":         2.0,
                               "max_deceleration":         6.0}

        self._controller = create_controller_by_name(controller, controller_params)
        self._control_spinner = Spinner(target = self._calc_control,
                                          rate = control_loop_rate)

        self._odometry = Odometry(self)
        self._odometry_spinner = Spinner(target = self._odometry.calc_odometry,
                                           rate = odometry_loop_rate)

        self._api_vehicle_mode = self.UNKNOWN
        self._vehicle_mode_check_spinner = Spinner(target = self._check_vehicle_mode,
                                                     rate = 1)
        self._vehicle_log = None
        self._vehicle_log_dir = OSCAR_DEFAULT_LOG_DIR
        self._vehicle_log_spinner = Spinner(target = self._log_vehicle_state,
                                              rate = OSCAR_DEFAULT_LOG_RATE)

        # self.start_odometry_calculation()


    def set_interface(self, interface):

        if self._vehicle_interface:
            self._stop_interface_communication()

        self._vehicle_interface = interface.create(interface)
        self._start_interface_communication()


    def start_controller(self):
        if (self._controller and (not self._control_spinner.is_active())):
                self._control_spinner.start()


    def stop_controller(self):
        self._control_spinner.stop()


    def set_controller(self, controller, params = None):

        controller_is_active = self._control_spinner.is_active()

        if controller_is_active:
            self.stop_controller()

        self._controller = create_controller_by_name(controller, params)

        if self._controller and controller_is_active:
            self.start_controller()


    def set_controller_params(self, params):
        if self._controller:
            self._controller.update_params(params)


    def set_controller_rate(self, rate):
        self._control_spinner.set_rate(rate)


    def get_actual_controller_rate(self):
        return self._control_spinner.get_real_rate()


    def _calc_control(self):

        cur_vehicle_velocity          = self._vehicle_protocol.get_vehicle_speed()
        cur_sw_angle, cur_sw_velocity = self._vehicle_protocol.get_steering_wheel_angle_and_velocity()
        cur_sw_torque, cur_eps_torque = self._vehicle_protocol.get_steering_wheel_and_eps_torques()

        # CALL CONTROL CALC STEP HERE
        throttle, sw_torque = 0, 0

        self._vehicle_protocol.set_vehicle_throttle(throttle)
        self._vehicle_protocol.set_steering_wheel_torque(sw_torque)


    def set_speed(self, speed = None, acceleration = None, jerk = None):
        if self._controller:
            self._controller.set_target_speed(speed = speed,
                                              acceleration = acceleration,
                                              jerk = jerk)


    def set_steering(self, steering_angle = None, steering_angle_velocity = None):
        if self._controller:
            self._controller.set_target_steering(steering_angle = steering_angle,
                                                 steering_angle_velocity = steering_angle_velocity)


    def set_vehicle_throttle(self, throttle):
        self._vehicle_protocol.set_vehicle_throttle(throttle)


    def set_steering_wheel_torque(self, steering_wheel_torque):
        self._vehicle_protocol.set_steering_wheel_torque(steering_wheel_torque)


    def start_odometry_calculation(self):
        if self._odometry_spinner.is_active():
            self._odometry_spinner.stop()
            self._odometry.reset()
        self._odometry_spinner.start()


    def stop_odometry_calculation(self):
        self._odometry_spinner.stop()


    def get_odometry(self):
        return self._odometry.get()


    def reset_odometry(self):
        self._odometry.reset()


    def set_odometry_calc_rate(self, rate):
        self._odometry_spinner.set_rate(rate)


    def get_actual_odometry_calc_rate(self):
        return self._odometry_spinner.get_real_rate()


    def auto_mode(self):

        if (self.get_mode() != self.VEHICLE_AUTO_MODE):

            if not self._vehicle_protocol.auto_mode():
                return False

        self._api_vehicle_mode = self.VEHICLE_AUTO_MODE
        self._vehicle_protocol.start_sending_vehicle_move_cmd()
        self._vehicle_protocol.start_sending_steering_wheel_torque_cmd()

        return True


    def manual_mode(self):

        self._vehicle_protocol.stop_sending_vehicle_move_cmd()
        self._vehicle_protocol.stop_sending_steering_wheel_torque_cmd()

        self._vehicle_protocol.set_vehicle_throttle(0)
        self._vehicle_protocol.set_steering_wheel_torque(0)

        self._api_vehicle_mode = self.VEHICLE_MANUAL_MODE

        if (self.get_mode() != self.VEHICLE_MANUAL_MODE):

            if not self._vehicle_protocol.manual_mode():
                return False

        return True


    def get_mode(self):
        mode, source = self._vehicle_protocol.get_mode()
        return mode


    def _check_vehicle_mode(self):
        mode, source = self._vehicle_protocol.get_mode()
        if self._api_vehicle_mode != mode:
            if mode == self.VEHICLE_AUTO_MODE:
                self.auto_mode()
            else:
                self.manual_mode()


    def emergency_stop(self):
        return self._vehicle_protocol.emergency_stop_on()


    def recover(self):
        return (self._vehicle_protocol.hand_brake_off() and
                self._vehicle_protocol.emergency_stop_off())


    def hand_brake(self):
        return self._vehicle_protocol.hand_brake_on()


    def led_blink(self):
        self._vehicle_protocol.led_reverse()
        for i in range(3):
            time.sleep(0.5)
            self._vehicle_protocol.led_reverse()
        return True


    def led_on(self):
        return self._vehicle_protocol.led_on()


    def led_off(self):
        return self._vehicle_protocol.led_off()


    def get_led(self):
        return self._vehicle_protocol.get_led()


    def left_turn_signal(self):
        self._vehicle_protocol.left_turn_signal()


    def right_turn_signal(self):
        self._vehicle_protocol.right_turn_signal()


    def emergency_signals(self):
        self._vehicle_protocol.emergency_signals()


    def turn_off_signals(self):
        self._vehicle_protocol.turn_off_signals()


    def get_emergency_stop(self):
        return self._vehicle_protocol.get_emergency_stop()


    def get_hand_brake(self):
        return self._vehicle_protocol.get_hand_brake()


    def get_vehicle_speed(self):
        return self._vehicle_protocol.get_vehicle_speed()


    def get_vehicle_wheels_speed(self):
        return self._vehicle_protocol.get_vehicle_wheels_speed()


    def get_steering_wheel_angle_and_velocity(self):
        return self._vehicle_protocol.get_steering_wheel_angle_and_velocity()


    def get_steering_wheel_and_eps_torques(self):
        return self._vehicle_protocol.get_steering_wheel_and_eps_torques()


    def vehicle_move_interception_on(self):
        return self._vehicle_protocol.vehicle_move_interception_on()


    def vehicle_move_interception_off(self):
        return self._vehicle_protocol.vehicle_move_interception_off()


    def start_sending_vehicle_move_cmd(self):
        return self._vehicle_protocol.start_sending_vehicle_move_cmd()


    def stop_sending_vehicle_move_cmd(self):
        return self._vehicle_protocol.stop_sending_vehicle_move_cmd()


    def steering_wheel_interception_on(self):
        return self._vehicle_protocol.steering_wheel_interception_on()


    def steering_wheel_interception_off(self):
        return self._vehicle_protocol.steering_wheel_interception_off()


    def start_sending_steering_wheel_torque_cmd(self):
        return self._vehicle_protocol.start_sending_steering_wheel_torque_cmd()


    def stop_sending_steering_wheel_torque_cmd(self):
        return self._vehicle_protocol.stop_sending_steering_wheel_torque_cmd()


    def error_report(self):
        return 'NO_ERROR'


    def _log_vehicle_state(self):
        cur_time = time.time()

        mode = self.get_mode()

        vehicle_speed         = self._vehicle_protocol.get_vehicle_speed()
        sw_angle, sw_velocity = self._vehicle_protocol.get_steering_wheel_angle_and_velocity()
        sw_torque, eps_torque = self._vehicle_protocol.get_steering_wheel_and_eps_torques()

        self._vehicle_log.add_data(cur_time,
                                   sw_angle,
                                   sw_velocity,
                                   sw_torque,
                                   eps_torque,
                                   vehicle_speed,
                                   mode)


    def start_vehicle_logger(self):
        self._vehicle_log = log.VehicleLog(self._vehicle_log_dir)
        self._vehicle_log_spinner.start()


    def change_vehicle_logger_dir(self, log_dir):
        self._vehicle_log_dir = log_dir


    def stop_vehicle_logger(self):
        self._vehicle_log_spinner.stop()
        self._vehicle_log.save()
        self._vehicle_log = None


class LexusRX450H(OscarVehicle):

    def __init__(self,  *args, **kwargs):
        super(LexusRX450H, self).__init__(*args, **kwargs)

        self.vehicle_params = {"wheel_radius":             0.37,
                               "wheel_width":              0.25,
                               "wheelbase":                2.75,
                               "axle_track":               1.64,
                               "steering_ratio":           14.8,
                               "max_steering_wheel_angle": 500,
                               "max_acceleration":         2.0,
                               "max_deceleration":         6.0}  # ~ 33.78 deg


class Odometry():

    def __init__(self, vehicle):

        self._vehicle = vehicle

        self.wheel_radius   = vehicle.vehicle_params["wheel_radius"]
        self.wheel_width    = vehicle.vehicle_params["wheel_width"]
        self.wheelbase      = vehicle.vehicle_params["wheelbase"]
        self.axle_track     = vehicle.vehicle_params["axle_track"]
        self.steering_ratio = vehicle.vehicle_params["steering_ratio"]

        self._pose_data_lock = threading.Lock()
        self.x    = 0.0
        self.y    = 0.0
        self.yaw  = 0.0
        self.dx   = 0.0
        self.dy   = 0.0
        self.dyaw = 0.0
        self.time = 0.0


    def get(self):
        return self.x, self.y, self.yaw, self.dx, self.dy, self.dyaw, self.time


    def reset(self):
        with self._pose_data_lock:
            self.x    = 0.0
            self.y    = 0.0
            self.yaw  = 0.0
            self.dx   = 0.0
            self.dy   = 0.0
            self.dyaw = 0.0
            self.time = 0.0


    def calc_odometry(self):

        cur_time = time.time()
        cur_vehicle_velocity          = self._vehicle.get_vehicle_speed()
        cur_sw_angle, cur_sw_velocity = self._vehicle.get_steering_wheel_angle_and_velocity()

        with self._pose_data_lock:

            dt = cur_time - self.time

            self.dx = cos(self.yaw) * cur_vehicle_velocity
            self.dy = sin(self.yaw) * cur_vehicle_velocity
            self.dyaw = cur_vehicle_velocity / self.wheelbase * tan(cur_sw_angle / self.steering_ratio)

            self.x += dt * self.dx
            self.y += dt * self.dy
            self.yaw += dt * self.dyaw

            self.time = cur_time


supported_vehicle_models = {"LEXUS_RX_450H": LexusRX450H}

def create_vehicle_by_model(vehicle_model      = None,
                            interface          = None,
                            protocol_config    = None,
                            controller         = None,
                            controller_params  = None,
                            control_loop_rate  = OSCAR_DEFAULT_CONTROL_RATE,
                            odometry_loop_rate = OSCAR_DEFAULT_ODOMETRY_CALC_RATE):

    if(vehicle_model == '' or vehicle_model is None):
        log.warning("Vehicle model was not specified!")
        return None

    elif (vehicle_model in supported_vehicle_models):
        try:
            return OscarVehicle(interface,
                                protocol_config,
                                controller,
                                controller_params,
                                control_loop_rate,
                                odometry_loop_rate)
        except Exception as e:
            log.warning(str(e) + "\n")
            return None

    else:
        log.warning("Vehicle model " + str(interface) + " is not supported!")
        return None
