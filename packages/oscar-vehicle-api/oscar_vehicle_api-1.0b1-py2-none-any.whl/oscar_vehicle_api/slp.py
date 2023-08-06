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

RAW_SLP_LEN = 26
SLP_HEADER_LEN  = 8
RECEIVE_SLP_HEADER = bytearray.fromhex('AAFF0110001000C1')
SEND_SLP_HEADER    = bytearray.fromhex('AA01FF100010001C')


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
    # print("crc8: " + hex(crc8))
    return bytearray([crc8])


# x^16 + x^12 + x^5 + x^0
def calc_crc16(data):

    crc16 = 0xFFFF

    for byte in data:
        crc16 ^= byte << 8

        for i in range(8):

            if (crc16 & 0x8000):
                xor_val = 0x1021
            else:
                xor_val = 0x0000

            crc16 = ((crc16 << 1) & 0x00FFFF) ^ xor_val

    slp_crc16 = bytearray([crc16 & 0x00FF, crc16>>8])

    return slp_crc16


def create_raw_slp_from_raw_oscar_data(raw_data):
    raw_slp_data = bytearray.fromhex('0101') + \
                   bytearray([raw_data[1]]) + \
                   bytearray([raw_data[0]]) + \
                   bytearray.fromhex('00000008') + \
                   raw_data[2:]
    raw_slp_data_crc = calc_crc16(raw_slp_data)
    raw_slp = SEND_SLP_HEADER + raw_slp_data + raw_slp_data_crc
    return raw_slp


def get_slp_data_from_raw_slp(raw):
    if ((len(raw) == RAW_SLP_LEN) and (raw[0:SLP_HEADER_LEN] == RECEIVE_SLP_HEADER)):
        return bytearray([raw[SLP_HEADER_LEN+3]]) + \
               bytearray([raw[SLP_HEADER_LEN+2]]) + \
               raw[SLP_HEADER_LEN+8:-2]
    else:
        return None


def slp_data_crc_is_ok(raw_slp_data, raw_slp_crc):
    if calc_crc16(raw_slp_data) == raw_slp_crc:
        return True
    else:
        return False


def print_raw(raw_data):
    print " ".join(hex(byte) for byte in raw_data)
