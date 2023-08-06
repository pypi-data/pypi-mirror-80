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

from math import copysign
import threading
import time

import log

OSCAR_CAN_V2 = 2
OSCAR_CAN_V3 = 3

UNKNOWN                   = 0x00
VEHICLE_AUTO_MODE         = 0x01
VEHICLE_MANUAL_MODE       = 0x02

# Commands CAN identifiers
STEERING_WHEEL_TORQUE_CMD_V2 = 0x7F9
VEHICLE_ACCELERATION_CMD_V2  = 0x7EE
LAUNCHER_CMD_V2              = 0x7FC
EMERGENCY_STOP_CMD_V2        = 0x7FC
HAND_BRAKE_CMD_V2            = 0x7FC
INFO_CONFIGURATION_CMD_V2    = 0x7FD
TURN_SIGNALS_CMD_V2          = 0x778

# Infos CAN identifiers
STEERING_WHEEL_POSE_VELOCITY_INFO_V2  = 0x25
STEERING_WHEEL_EPS_TORQUE_INFO_V2     = 0x260
STEERING_WHEEL_TORQUE_INFO_V2         = 0x7F1
STEERING_WHEEL_INTERCEPTION_INFO_V2   = 0x7F1
VEHICLE_SPEED_INFO_V2                 = 0xB4
VEHICLE_WHEELS_SPEED_INFO_V2          = 0xAA
VEHICLE_MOVING_INTERCEPTION_INFO_V2   = 0x7F5
LAUNCHER_INFO_V2                      = 0x7F6
EMERGENCY_STOP_INFO_V2                = 0x7F6
HAND_BRAKE_INFO_V2                    = 0x7F6


class OscarProtocolConfig():
    """
    Functionality-oriented protocol configuration structure.
    """
    def __init__(self, version = OSCAR_CAN_V2):

        self.version = version

        self.vehicle_speed_info_need_to_receive                = True
        self.vehicle_wheels_speed_info_need_to_receive         = False
        self.vehicle_moving_interception_info_need_to_receive  = True

        self.steering_wheel_pose_velocity_info_need_to_receive = True
        self.steering_wheel_eps_torques_info_need_to_receive   = True
        self.steering_wheel_torque_info_need_to_receive        = True
        self.steering_wheel_interception_info_need_to_receive  = True

        self.launcher_info_need_to_receive                     = True
        self.emergency_stop_info_need_to_receive               = True
        self.hand_brake_info_need_to_receive                   = True

        self.steering_wheel_torque_cmd_send_rate               = 60.0
        self.vehicle_move_cmd_send_rate                        = 60.0
        self.emergency_stop_cmd_rate                           = 30.0

        self.launcher_info_rate                     = 2.0
        self.emergency_stop_info_rate               = 2.0
        self.hand_brake_info_rate                   = 2.0

        self.vehicle_moving_interception_info_rate  = 2.0
        self.steerin_wheel_interception_info_rate   = 2.0

        self.vehicle_speed_info_rate                = 80.0

        self.steering_wheel_pose_velocity_info_rate = 80.0
        self.steering_wheel_torque_info_rate        = 80.0


class OscarProtocol():

    SEND_ONCE = 1
    SEND_ONCE_NEED_REPLY = 2
    SEND_CONSTANTLY = 3
    SEND_CONSTANTLY_NEED_REPLY = 4

    RECEIVE_ONCE = 1
    RECEIVE_CONSTANTLY = 2


    def __init__(self, config = None):

        # All commands handlers
        self.steering_wheel_torque_cmd = None
        self.vehicle_move_cmd  = None

        self.launcher_cmd              = None
        self.emergency_stop_cmd        = None
        self.hand_brake_cmd            = None

        self.turn_signals_cmd          = None

        self.info_configuration_cmd    = None

        # All infos handlers

        self.vehicle_speed_info                = None
        self.vehicle_wheels_speed_info         = None
        self.vehicle_moving_interception_info  = None

        self.steering_wheel_pose_velocity_info = None
        self.steering_wheel_eps_torques_info   = None
        self.steering_wheel_torque_info        = None
        self.steering_wheel_interception_info  = None

        self.launcher_info                     = None
        self.emergency_stop_info               = None
        self.hand_brake_info                   = None

        self._send_list_lock    = threading.Lock()
        self._receive_list_lock = threading.Lock()

        self._send_list    = {}
        self._receive_list = {}

        self._identifier_counter = 0

        self._configure(config)


    def _configure(self, config):

        if not config:
            config = OscarProtocolConfig()
            log.warning("Default OSCAR Protocol configuration (OSCAR_CAN_V2)")

        if config.version == OSCAR_CAN_V2:

            # All commands handlers
            self.steering_wheel_torque_cmd       = OscarSteeringWheelTorqueCmdDataV2(self)
            self.steering_wheel_interception_cmd = OscarSteeringWheelTorqueCmdDataV2(self)

            self.vehicle_move_cmd                = OscarVehicleMoveCmdDataV2(self)
            self.vehicle_move_interception_cmd   = OscarVehicleMoveCmdDataV2(self)

            self.info_configuration_cmd          = OscarInfoConfigurationCmdDataV2(self)

            self.launcher_cmd                    = OscarLauncherCmdDataV2(self)
            self.emergency_stop_cmd              = OscarLauncherCmdDataV2(self)
            self.hand_brake_cmd                  = OscarLauncherCmdDataV2(self)

            self.turn_signals_cmd                = OscarTurnSignalsCmdDataV2(self)

            # All infos handlers
            self.vehicle_speed_info                = OscarVehicleSpeedInfoDataV2(self)
            self.vehicle_wheels_speed_info         = OscarVehicleWheelsSpeedInfoDataV2(self)
            # self.vehicle_moving_interception_info  = OscarDsuLkaInterceptionInfoDataV2(self)

            self.steering_wheel_pose_velocity_info = OscarSteeringWheelPoseVelocityInfoDataV2(self)
            self.steering_wheel_eps_torques_info   = OscarSteeringWheelEpsTorquesInfoDataV2(self)
            # self.steering_wheel_torque_info        = OscarSteeringWheelTorqueInfoDataV2(self)
            # self.steering_wheel_interception_info  = self.steering_wheel_torque_info

            self.launcher_info                     = OscarLauncherInfoDataV2(self)
            self.emergency_stop_info               = self.launcher_info
            self.hand_brake_info                   = self.launcher_info

        # All commands setting up
        self.steering_wheel_torque_cmd.set_send_rate(config.steering_wheel_torque_cmd_send_rate)
        self.vehicle_move_cmd.set_send_rate(config.vehicle_move_cmd_send_rate)
        self.emergency_stop_cmd.set_send_rate(config.emergency_stop_cmd_rate)

        # All infos setting up
        if config.vehicle_speed_info_need_to_receive:
            self.vehicle_speed_info.start_receiving()

        if config.vehicle_wheels_speed_info_need_to_receive:
            self.vehicle_wheels_speed_info.start_receiving()

        if config.steering_wheel_pose_velocity_info_need_to_receive:
            self.steering_wheel_pose_velocity_info.start_receiving()

        if config.steering_wheel_eps_torques_info_need_to_receive:
            self.steering_wheel_eps_torques_info.start_receiving()

        if config.launcher_info_need_to_receive:    # emergency_stop and hand_brake
            self.launcher_info.start_receiving()
            self.launcher_info.set_receive_rate(config.launcher_info_rate)


    def _get_identifier(self):
        identifier = self._identifier_counter
        self._identifier_counter += 1
        return identifier


    def _copy_data(self, data):
        new_data = globals()[data.__class__.__name__](self)
        new_data._can_data  = data._can_data
        new_data._send_type = data._send_type
        return new_data


    def _register_to_send_list(self, data):
        with self._send_list_lock:
            if data._send_type == self.SEND_ONCE:
                data = self._copy_data(data)
                data._identifier = self._get_identifier()
            self._send_list.update({data._identifier: data})


    def _get_actual_need_to_send_data(self):
        current_time = time.time()
        need_to_send_list = {}
        with self._send_list_lock:
            for data in self._send_list.itervalues():
                data_time_left = data._next_send_time - current_time

                if (data_time_left <= 0.0):
                    need_to_send_list.update({data._identifier: data})

        return need_to_send_list


    def _unregister_from_send_list(self, data):
        with self._send_list_lock:
            self._send_list.pop(data._identifier, None)


    def _register_to_receive_list(self, data):
        self._receive_list.update({data._get_can_id(): data})


    def _unregister_from_receive_list(self, data):
        self._receive_list.pop(data._get_can_id(), None)


    def _configure_received_infos_rate(self, data, rate):
        if self.info_configuration_cmd:
            if rate > 0:
                self.info_configuration_cmd.set_reply_delay(data, 1 / rate)
            else:
                self.info_configuration_cmd.turn_off_replies(data)
            return True
        else:
            return False


    def get_raw_data_to_send(self):
        """
        Return array of protocol raw data which have to be sent by interface.
        """
        raw_data_frames_to_send = []
        need_to_send_data_list = self._get_actual_need_to_send_data()

        if need_to_send_data_list:
            current_time = time.time()
            for data in need_to_send_data_list.itervalues():
                data_time_left = data._next_send_time - current_time
                raw_data_frames_to_send.append(data.raw())

                if data._send_type == self.SEND_CONSTANTLY:
                    data._next_send_time = current_time + 1./data._send_rate
                    data._real_send_rate = data._send_rate + data_time_left

                elif data._send_type == self.SEND_ONCE:
                    self._unregister_from_send_list(data)

        return raw_data_frames_to_send


    def update_data_from_raw(self, raws, receive_time = 0.0):

        for raw in raws:
            can_id = raw[1] + (raw[0] << 8)
            if can_id in self._receive_list:
                self._receive_list[can_id].update_from_raw(raw, receive_time)


    def auto_mode(self):
        self.launcher_cmd.auto_mode()
        return True


    def manual_mode(self):
        self.launcher_cmd.manual_mode()
        return True


    def get_mode(self):
        return self.launcher_info.get_mode()


    def emergency_stop_on(self):
        self.emergency_stop_cmd.emergency_stop_on()
        return True


    def emergency_stop_off(self):
        self.emergency_stop_cmd.emergency_stop_off()
        return True


    def get_emergency_stop(self):
        emergency_stop_state, source = self.launcher_info.get_emergency_stop()
        return (emergency_stop_state == self.launcher_info.EMERGENCY_STOP_ON)


    def hand_brake_on(self):
        self.hand_brake_cmd.hand_brake_on()
        return True


    def hand_brake_off(self):
        self.hand_brake_cmd.hand_brake_off()
        return True


    def get_hand_brake(self):
        hand_brake_state, source = self.launcher_info.get_hand_brake()
        return (hand_brake_state == self.launcher_info.HAND_BRAKE_ON)


    def led_on(self):
        self.launcher_cmd.led_on()
        return True


    def led_off(self):
        self.launcher_cmd.led_off()
        return True


    def get_led(self):
        return (self.launcher_info.get_led() == self.launcher_info.LED_ON)


    def led_reverse(self):
        if (self.launcher_info.get_led() == self.launcher_info.LED_ON):
            self.launcher_cmd.led_off()
        else:
            self.launcher_cmd.led_on()


    def left_turn_signal(self):
        self.turn_signals_cmd.left_signal()


    def right_turn_signal(self):
        self.turn_signals_cmd.right_signal()


    def emergency_signals(self):
        self.turn_signals_cmd.emergency_signals()


    def turn_off_signals(self):
        self.turn_signals_cmd.turn_off_signals()


    def vehicle_move_interception_on(self):
        self.vehicle_move_interception_cmd.interception_on()
        return True


    def vehicle_move_interception_off(self):
        self.vehicle_move_interception_cmd.interception_off()
        return True


    def start_sending_vehicle_move_cmd(self):
        self.vehicle_move_cmd.start_sending()
        return True


    def stop_sending_vehicle_move_cmd(self):
        self.vehicle_move_cmd.stop_sending()
        return True


    def set_vehicle_throttle(self, throttle):
        self.vehicle_move_cmd.throttle(throttle)


    def get_vehicle_speed(self):
        return self.vehicle_speed_info.get_vehicle_speed()


    def get_vehicle_wheels_speed(self):
        return self.vehicle_wheels_speed_info.get_vehicle_wheels_speed()


    def steering_wheel_interception_on(self):
        self.steering_wheel_interception_cmd.interception_on()
        return True


    def steering_wheel_interception_off(self):
        self.steering_wheel_interception_cmd.interception_off()
        return True


    def start_sending_steering_wheel_torque_cmd(self):
        self.steering_wheel_torque_cmd.start_sending()
        return True


    def stop_sending_steering_wheel_torque_cmd(self):
        self.steering_wheel_torque_cmd.stop_sending()
        return True


    def set_steering_wheel_torque(self, steering_wheel_torque):
        self.steering_wheel_torque_cmd.torque(steering_wheel_torque)


    def get_steering_wheel_angle_and_velocity(self):
        return self.steering_wheel_pose_velocity_info.get_steering_wheel_angle_and_velocity()


    def get_steering_wheel_and_eps_torques(self):
        return self.steering_wheel_eps_torques_info.get_steering_wheel_and_eps_torques()



class OscarData(object):

    CAN_TYPE_INFO = bytearray.fromhex("01")
    CAN_TYPE_CMD  = bytearray.fromhex("02")
    CAN_TYPE_ACK  = bytearray.fromhex("03")

    CAN_STATE_UNKNOWN             = bytearray.fromhex("00")
    CAN_STATE_WORK_AND_ACTIVE     = bytearray.fromhex("01")
    CAN_STATE_WORK_BUT_NOT_ACTIVE = bytearray.fromhex("02")
    CAN_STATE_ERROR               = bytearray.fromhex("03")
    CAN_STATE_DEBUG               = bytearray.fromhex("04")

    def __init__(self, protocol):
        self._protocol = protocol
        self._identifier = self._protocol._get_identifier()

        self._send_rate = -1
        self._real_send_rate = 0.0
        self._next_send_time = 0.0
        self._send_type = None

        self._receive_rate = None
        self._real_receive_rate = 0.0
        self._last_receive_time = 0.0
        self._receive_type = None

        self._can_data_lock = threading.Lock()
        self._can_id        = bytearray.fromhex("0000")
        self._can_cnc       = bytearray.fromhex("FF")
        self._can_type      = bytearray.fromhex("00")
        self._can_data      = bytearray.fromhex("00000000")
        self._can_state     = bytearray.fromhex("00")
        self._can_crc       = bytearray.fromhex("00")


    def _set_can_id(self, can_id):
        self._can_id = bytearray([can_id>>8, can_id & 0x00FF])


    def _get_can_id(self):
        return self._can_id[1] + (self._can_id[0] << 8)


    def _get_identifier(self):
        return self._identifier


    def _set_can_cnc(self, can_cnc):
        self._can_cnc[0] = can_cnc


    def _increment_can_cnc(self, can_cnc):
        if self._can_cnc[0] == 0xFE:
            self._can_cnc[0] = 0x00
        else:
            self._can_cnc[0] += 0x01


    def _reset_can_cnc(self):
        self._can_cnc[0] = 0x00


    def _unset_can_cnc(self):
        self._can_cnc[0] = 0xFF


    def _get_can_cnc(self):
        return self._can_cnc[0]


    def _set_can_type(self, can_type):
        self._can_type = can_type


    def _get_can_type(self):
        return self._can_type


    def _set_can_data(self, can_data):
        with self._can_data_lock:
            self._can_data = can_data


    def _reset_can_data(self):
        with self._can_data_lock:
            self._can_data = bytearray.fromhex("00000000")


    def _get_can_data(self):
        with self._can_data_lock:
            return self._can_data


    def _set_can_state(self, can_state):
        self._can_state = can_state


    def _get_can_state(self):
        return self._can_state


    def _calc_crc(self):
        try:
            self._can_crc = calc_crc8(self._can_id +
                                      self._can_cnc +
                                      self._can_type +
                                      self._can_data +
                                      self._can_state)
        except Exception as e:
            print(e)


    def send_once(self):
        self._send_type = self._protocol.SEND_ONCE
        self._protocol._register_to_send_list(self)


    def start_sending(self):
        if (0 < self._send_rate):
            self._send_type = self._protocol.SEND_CONSTANTLY
            self._protocol._register_to_send_list(self)
            return True
        else:
            return False


    def stop_sending(self):
        self._protocol._unregister_from_send_list(self)


    def set_send_rate(self, rate):
        if (0.0 < rate):
            self._send_rate = rate
            return True
        else:
            return False


    def get_send_rate(self):
        return self._send_rate


    def get_real_send_rate(self):
        return self._real_send_rate


    def receive_once(self):
        self._receive_type = self._protocol.RECEIVE_ONCE
        self._protocol._register_to_receive_list(self)


    def start_receiving(self):
        self._receive_type = self._protocol.RECEIVE_CONSTANTLY
        self._protocol._register_to_receive_list(self)


    def stop_receiving(self):
        self._protocol._unregister_from_receive_list(self)


    def set_receive_rate(self, rate):
        if self._protocol._configure_received_infos_rate(self, rate):
            self._receive_rate = rate


    def get_last_receive_time(self):
        return self._last_receive_time



    def update_from_raw(self, raw, receive_time = None):

        if receive_time:
            delay = receive_time - self._last_receive_time
            if delay != 0:
                self._real_receive_rate = 1 / (delay)
                self._last_receive_time = receive_time

        self._can_cnc = raw[2]
        self._can_data = raw[4:8]
        self._can_state = raw[8]
        self._can_crc =  raw[9]


    def raw(self):
        self._calc_crc()
        return self._can_id + \
               self._can_cnc + \
               self._can_type + \
               self._can_data + \
               self._can_state + \
               self._can_crc


class OscarCmdData(OscarData):
    """
    Command data type
    """
    def __init__(self,  *args, **kwargs):
        super(OscarCmdData, self).__init__(*args, **kwargs)


class OscarInfoData(OscarData):
    """
    Info / Status data type
    """
    def __init__(self,  *args, **kwargs):
        super(OscarInfoData, self).__init__(*args, **kwargs)


class OscarAckData(OscarData):
    """
    Acknowledgment / Confirmation data type
    """
    def __init__(self,  *args, **kwargs):
        super(OscarAckData, self).__init__(*args, **kwargs)


# ----------------------- OSCAR_CAN_V2 -----------------------------------------

class OscarSteeringWheelTorqueCmdDataV2(OscarCmdData):
    """
    Steering Wheel Control by Torque Command data type
    """

    DONT_CHANGE      = 0x00
    INTERCEPTION_ON  = 0x01
    INTERCEPTION_OFF = 0x02

    LEFT_DIRECTION  = 0x02
    RIGHT_DIRECTION = 0x01

    MAX_TORQUE = 1000

    def __init__(self,  *args, **kwargs):
        super(OscarSteeringWheelTorqueCmdDataV2, self).__init__(*args, **kwargs)

        self._set_can_id(STEERING_WHEEL_TORQUE_CMD_V2)
        self._can_type  = OscarData.CAN_TYPE_CMD
        self._can_state = OscarData.CAN_STATE_WORK_AND_ACTIVE


    def _set_interception(self, interception):
        self._can_data[0] = interception


    def interception_on(self):
        self._reset_can_data()
        self._set_interception(self.INTERCEPTION_ON)
        self.send_once()


    def interception_off(self):
        self._reset_can_data()
        self._set_interception(self.INTERCEPTION_OFF)
        self.send_once()


    def _set_direction(self, direction):
        self._can_data[1] = direction


    def _set_torque(self, torque):

        if torque > 0:
            self._set_direction(self.LEFT_DIRECTION)
        else:
            self._set_direction(self.RIGHT_DIRECTION)

        torque = min(int(abs(torque * 10)), self.MAX_TORQUE)
        self._can_data[2] = torque & 0x00FF
        self._can_data[3] = torque >> 8


    def torque(self, torque):
        self._set_torque(torque)


class OscarVehicleMoveCmdDataV2(OscarCmdData):
    """
    Steering Wheel Control by Torque Command data type
    """

    DONT_CHANGE      = 0x00
    INTERCEPTION_ON  = 0x01
    INTERCEPTION_OFF = 0x02

    LEFT_DIRECTION  = 0x02
    RIGHT_DIRECTION = 0x01

    MAX_THROTTLE = 1000

    def __init__(self,  *args, **kwargs):
        super(OscarVehicleMoveCmdDataV2, self).__init__(*args, **kwargs)

        self._set_can_id(VEHICLE_ACCELERATION_CMD_V2)
        self._can_type  = OscarData.CAN_TYPE_CMD
        self._can_state = OscarData.CAN_STATE_WORK_AND_ACTIVE


    def _set_interception(self, interception):
        self._can_data[0] = interception


    def interception_on(self):
        self._reset_can_data()
        self._set_interception(self.INTERCEPTION_ON)
        self.send_once()


    def interception_off(self):
        self._reset_can_data()
        self._set_interception(self.INTERCEPTION_OFF)
        self.send_once()


    def throttle(self, throttle):
        if throttle > 0:
            throttle = int(min(throttle * 10,  self.MAX_THROTTLE))
        else:
            throttle = int(max(throttle * 10, -self.MAX_THROTTLE)) & 0xFFFF

        self._can_data[1] = throttle & 0x00FF
        self._can_data[2] = throttle >> 8


class OscarLauncherCmdDataV2(OscarCmdData):
    """
    Launcher and LED Command data type
    """

    MODE_DONT_CHANGE = 0x00
    MODE_AUTO        = 0x01
    MODE_RADIO_JOY   = 0x02
    MODE_MANUAL      = 0x03

    LED_DONT_CHANGE = 0x00
    LED_ON          = 0x01
    LED_OFF         = 0x02

    EMERGENCY_STOP_DONT_CHANGE = 0x00
    EMERGENCY_STOP_ON          = 0x01
    EMERGENCY_STOP_OFF         = 0x02

    HAND_BRAKE_DONT_CHANGE = 0x00
    HAND_BRAKE_ON          = 0x01
    HAND_BRAKE_OFF         = 0x02

    def __init__(self,  *args, **kwargs):
        super(OscarLauncherCmdDataV2, self).__init__(*args, **kwargs)

        self._set_can_id(LAUNCHER_CMD_V2)
        self._can_type  = OscarData.CAN_TYPE_CMD
        self._can_state = OscarData.CAN_STATE_WORK_AND_ACTIVE


    def _set_mode(self, mode):
        with self._can_data_lock:
            self._can_data[0] = mode


    def auto_mode(self):
        self._reset_can_data()
        self._set_mode(self.MODE_AUTO)
        self.send_once()


    def manual_mode(self):
        self._reset_can_data()
        self._set_mode(self.MODE_MANUAL)
        self.send_once()


    def _set_led(self, led):
        with self._can_data_lock:
            self._can_data[1] = led


    def led_on(self):
        self._reset_can_data()
        self._set_led(self.LED_ON)
        self.send_once()


    def led_off(self):
        self._reset_can_data()
        self._set_led(self.LED_OFF)
        self.send_once()


    def led_reverse(self):
        # got current LED state from self._protocol.launcher_info.get_led_state()
        pass


    def _set_emergency_stop(self, emergency_stop):
        with self._can_data_lock:
            self._can_data[2] = emergency_stop


    def emergency_stop_on(self):
        self._reset_can_data()
        self._set_emergency_stop(self.EMERGENCY_STOP_ON)
        self.send_once()


    def emergency_stop_off(self):
        self._reset_can_data()
        self._set_emergency_stop(self.EMERGENCY_STOP_OFF)
        self.send_once()


    def _set_hand_brake(self, hand_brake):
        with self._can_data_lock:
            self._can_data[3] = hand_brake


    def hand_brake_on(self):
        self._reset_can_data()
        self._set_hand_brake(self.HAND_BRAKE_ON)
        self.send_once()


    def hand_brake_off(self):
        self._reset_can_data()
        self._set_hand_brake(self.HAND_BRAKE_OFF)
        self.send_once()


class OscarTurnSignalsCmdDataV2(OscarCmdData):

    TURN_SIGNALS_DONT_CHANGE = 0x00
    RIGHT_TURN_SIGNAL        = 0x01
    LEFT_TURN_SIGNAL         = 0x02
    EMERGENCY_SIGNALS        = 0x03
    TURN_OFF_SIGNALS         = 0x04

    def __init__(self,  *args, **kwargs):
        super(OscarTurnSignalsCmdDataV2, self).__init__(*args, **kwargs)

        self._set_can_id(TURN_SIGNALS_CMD_V2)
        self._can_type  = OscarData.CAN_TYPE_CMD
        self._can_state = OscarData.CAN_STATE_WORK_AND_ACTIVE


    def _set_signal(self, signal):
        with self._can_data_lock:
            self._can_data[0] = signal


    def left_signal(self):
        self._reset_can_data()
        self._set_signal(self.LEFT_TURN_SIGNAL)
        self.send_once()


    def right_signal(self):
        self._reset_can_data()
        self._set_signal(self.RIGHT_TURN_SIGNAL)
        self.send_once()


    def emergency_signals(self):
        self._reset_can_data()
        self._set_signal(self.EMERGENCY_SIGNALS)
        self.send_once()


    def turn_off_signals(self):
        self._reset_can_data()
        self._set_signal(self.TURN_OFF_SIGNALS)
        self.send_once()


class OscarInfoConfigurationCmdDataV2(OscarCmdData):
    """
    Launcher and LED Command data type
    """

    DONT_CHANGE     = 0x00
    MODULE_TURN_ON  = 0x01
    MODULE_TURN_OFF = 0x02
    MODULE_RESTART  = 0x03
    SET_DELAY       = 0x04

    def __init__(self,  *args, **kwargs):
        super(OscarInfoConfigurationCmdDataV2, self).__init__(*args, **kwargs)

        self._set_can_id(INFO_CONFIGURATION_CMD_V2)
        self._can_type  = OscarData.CAN_TYPE_CMD
        self._can_state = OscarData.CAN_STATE_WORK_AND_ACTIVE


    def _set_module_cmd(self, cmd):
        with self._can_data_lock:
            self._can_data[3] = cmd


    def _set_module_can_id(self, can_id):
        with self._can_data_lock:
            self._can_data[0] = can_id[0]
            self._can_data[1] = can_id[1]


    def _set_delay(self, delay):
        with self._can_data_lock:
            delay = min(int(abs(delay) * 1000), 2500)
            if (delay > 0) and (delay < 10):
                delay = 10
            self._can_data[2] = delay/10


    def set_reply_delay(self, oscar_info_data, delay):
        self._reset_can_data()
        self._set_module_cmd(self.SET_DELAY)
        self._set_delay(delay)
        self._set_module_can_id(oscar_info_data._can_id)
        self.send_once()


    def turn_off_replies(self, oscar_info_data):
        self._reset_can_data()
        self._set_module_cmd(self.SET_DELAY)
        self._set_delay(0)
        self._set_module_can_id(oscar_info_data._can_id)
        self.send_once()


class OscarLauncherInfoDataV2(OscarInfoData):
    """
    Launcher, LED, Emergency stop and Hand brake Info / Status data type
    """

    UNKNOWN   = 0x00

    MODE_AUTO         = VEHICLE_AUTO_MODE
    MODE_MANUAL       = VEHICLE_MANUAL_MODE
    MODE_RADIO_JOY    = 0x03

    SOURCE_VEHICLE = 0x01
    SOURCE_BUTTON  = 0x02
    SOURCE_REMOTE  = 0x03
    SOURCE_AUTO    = 0x04
    SOURCE_CMD     = 0x05

    LED_ON      = 0x01
    LED_OFF     = 0x02

    EMERGENCY_STOP_ON  = 0x01
    EMERGENCY_STOP_OFF = 0x02

    HAND_BRAKE_ON  = 0x01
    HAND_BRAKE_OFF = 0x02

    def __init__(self,  *args, **kwargs):
        super(OscarLauncherInfoDataV2, self).__init__(*args, **kwargs)
        self._set_can_id(LAUNCHER_INFO_V2)
        self._can_type = OscarData.CAN_TYPE_INFO


    def get_mode(self):

        with self._can_data_lock:
            button = self._can_data[0]

        source = (button & 0b00111000) >> 3
        mode = (button & 0b00000111)

        return mode, source


    def get_led(self):
        with self._can_data_lock:
            return self._can_data[1]


    def get_emergency_stop(self):

        with self._can_data_lock:
            emergency_stop = self._can_data[2]

        source = (emergency_stop & 0b00111000) >> 3
        state = (emergency_stop & 0b00000111)

        return state, source


    def get_hand_brake(self):

        with self._can_data_lock:
            hand_brake = self._can_data[3]

        source = (hand_brake & 0b00111000) >> 3
        state = (hand_brake & 0b00000111)

        return state, source


class OscarVehicleSpeedInfoDataV2(OscarInfoData):

    def __init__(self,  *args, **kwargs):
        super(OscarVehicleSpeedInfoDataV2, self).__init__(*args, **kwargs)
        self._set_can_id(VEHICLE_SPEED_INFO_V2)
        self._can_type = OscarData.CAN_TYPE_INFO
        self._can_data = bytearray.fromhex("0000000000000000")


    def get_vehicle_speed(self):
        with self._can_data_lock:
            speed_h, speed_l = self._can_data[5], self._can_data[6]

        return ((speed_h << 8) + speed_l) / 3.6 / 100.


    def get_vehicle_encoder(self):    # 6-8 wheels turns for 256 ticks
        return self._can_data[4]      # works from some speed


    def update_from_raw(self,raw, receive_time = None):

        if receive_time:
            delay = receive_time - self._last_receive_time
            if delay != 0:
                self._real_receive_rate = 1 / (delay)
                self._last_receive_time = receive_time

        self._can_data = raw[2:10]


class OscarVehicleWheelsSpeedInfoDataV2(OscarInfoData):

    def __init__(self,  *args, **kwargs):
        super(OscarVehicleWheelsSpeedInfoDataV2, self).__init__(*args, **kwargs)
        self._set_can_id(VEHICLE_WHEELS_SPEED_INFO_V2)
        self._can_type = OscarData.CAN_TYPE_INFO
        self._can_data = bytearray.fromhex("0000000000000000")


    def get_vehicle_wheels_speed(self):
        with self._can_data_lock:
            fr_h, fr_l = self._can_data[0], self._can_data[1]
            fl_h, fl_l = self._can_data[2], self._can_data[3]
            fr_h, fr_l = self._can_data[4], self._can_data[5]
            fl_h, fl_l = self._can_data[6], self._can_data[7]

        return ((((fr_h << 8) + fr_l) * 0.01 - 67.67) / 3.6, #FR
                (((fl_h << 8) + fl_l) * 0.01 - 67.67) / 3.6, #FL
                (((fr_h << 8) + fr_l) * 0.01 - 67.67) / 3.6, #RR
                (((fl_h << 8) + fl_l) * 0.01 - 67.67) / 3.6) #RL


    def update_from_raw(self, raw, receive_time = None):

        if receive_time:
            delay = receive_time - self._last_receive_time
            if delay != 0:
                self._real_receive_rate = 1 / (delay)
                self._last_receive_time = receive_time

        self._can_data = raw[2:10]


class OscarSteeringWheelPoseVelocityInfoDataV2(OscarInfoData):

    def __init__(self,  *args, **kwargs):
        super(OscarSteeringWheelPoseVelocityInfoDataV2, self).__init__(*args, **kwargs)
        self._set_can_id(STEERING_WHEEL_POSE_VELOCITY_INFO_V2)
        self._can_type = OscarData.CAN_TYPE_INFO
        self._can_data = bytearray.fromhex("0000000000000000")


    def get_steering_wheel_angle(self):
        with self._can_data_lock:
            sw_angle_h, sw_angle_l = self._can_data[0], self._can_data[1]
        return 1.5 * twos_complement((sw_angle_h << 8) + sw_angle_l, 12)


    def get_steering_wheel_velocity(self):
        with self._can_data_lock:
            sw_velocity_h, sw_velocity_l = self._can_data[4], self._can_data[5]
        return twos_complement((sw_velocity_h << 8) + sw_velocity_l, 12)


    def get_steering_wheel_angle_and_velocity(self):

        with self._can_data_lock:
            sw_angle_h, sw_angle_l = self._can_data[0]  & 0x0F, self._can_data[1]
            sw_velocity_h, sw_velocity_l = self._can_data[4] & 0x0F, self._can_data[5]

        return (1.5 * twos_complement((sw_angle_h << 8) + sw_angle_l, 12),
                twos_complement((sw_velocity_h << 8) + sw_velocity_l, 12))


    def get_steering_fraction(self):
        return 0.1 * twos_complement(self._can_data[4] >> 4, 4)


    def update_from_raw(self, raw, receive_time = None):

        self._can_data = raw[2:10]

        if receive_time:
            delay = receive_time - self._last_receive_time
            if delay != 0:
                self._real_receive_rate = 1 / (delay)
                self._last_receive_time = receive_time


class OscarSteeringWheelEpsTorquesInfoDataV2(OscarInfoData):

    def __init__(self,  *args, **kwargs):
        super(OscarSteeringWheelEpsTorquesInfoDataV2, self).__init__(*args, **kwargs)
        self._set_can_id(STEERING_WHEEL_EPS_TORQUE_INFO_V2)
        self._can_type = OscarData.CAN_TYPE_INFO
        self._can_data = bytearray.fromhex("0000000000000000")


    def get_steering_wheel_torque(self):
        with self._can_data_lock:
            sw_torque_h, sw_torque_l = self._can_data[1], self._can_data[2]

        return twos_complement((sw_torque_h << 8) + sw_torque_l, 16) # [-32768 | 32767]


    def get_eps_torque(self):
        with self._can_data_lock:
            eps_h, eps_l = self._can_data[5], self._can_data[6]

        return 0.73 * twos_complement((eps_h << 8) + eps_l, 16) # [-20000 | 20000]


    def get_steering_wheel_and_eps_torques(self):

        with self._can_data_lock:
            sw_torque_h, sw_torque_l = self._can_data[1], self._can_data[2]
            eps_h, eps_l             = self._can_data[5], self._can_data[6]

        return (twos_complement((sw_torque_h << 8) + sw_torque_l, 16),
                0.73 * twos_complement((eps_h << 8) + eps_l, 16))


    def update_from_raw(self, raw, receive_time = None):

        if receive_time:
            delay = receive_time - self._last_receive_time
            if delay != 0:
                self._real_receive_rate = 1 / (delay)
                self._last_receive_time = receive_time

        self._can_data = raw[2:10]


# ----------------------- OSCAR_CAN_V3 -----------------------------------------
# TODO
#--------------------

# x^8 + x^2 + x^1 + x^0
def calc_crc8(data):

    crc8 = 0xFF

    for byte in data:
        crc8 ^= byte

        for i in range(8):

            if (crc8 & 0x80):
                xor_val = 0x07
            else:
                xor_val = 0x00

            crc8 = ((crc8 << 1) & 0x00FF) ^ xor_val

    return bytearray([crc8])


def twos_complement(value, bits):
    if value & (1 << (bits-1)):
        value -= 1 << bits
    return value
