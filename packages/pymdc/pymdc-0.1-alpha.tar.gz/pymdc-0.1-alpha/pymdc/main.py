# -*- coding: utf-8 -*-

import logging
import socket

from .const import (
    BUFFER_SIZE,
    GET_VOLUME,
    HEADER,
    POWER_ON,
    POWER_OFF,
    POWER_STATUS,
    SENSOR_HEATEX,
    SENSOR_LED_PLATE,
    GET_MODEL,
)

_LOGGER = logging.getLogger(__name__)


class MDC:
    """ Multiple Display Control class """

    def __init__(self, host, port=1515, unit_id=0x00):

        self._host = host
        self._port = int(port)
        self._id = unit_id

        self.connected = False

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _calculate_checksum(self, data):
        return sum(data) % 256

    def _parse_response(self, data):
        pass

    def _connect(self):
        if not self.connected:
            self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._s.connect((self._host, self._port))
            self.connected = True

    def _disconnect(self):
        self.connected = False
        self._s.close()

    def _assemble_cmd(self, cmd, data=None):
        """ takes in the main command and arguments and
        assemble the complete command """

        if data is not None:
            # until i have figured this out, let's just set the length to 1
            datalen = 0x01

            msg = [
                HEADER,
                cmd,
                self._id,
                datalen,
                data
            ]

        else:
            datalen = 0x00

            msg = [
                HEADER,
                cmd,
                self._id,
                datalen
            ]

        msg.append(self._calculate_checksum(msg[1:]))

        return msg

    def volume(self):
        self._connect()
        msg = self._assemble_cmd(GET_VOLUME[0])

        self._s.send(bytes(msg))
        data = self._s.recv(BUFFER_SIZE)

        self._disconnect()

        return(data)

    def power_status(self):

        self._connect()

        msg = self._assemble_cmd(
            POWER_STATUS[0]
        )

        self._s.send(bytes(msg))

        data = self._s.recv(BUFFER_SIZE)

        self._disconnect()

        if chr(data[4]) == 'A':
            if data[6]:
                return True
            else:
                return False

    def power_on(self):

        self._connect()

        msg = self._assemble_cmd(
            POWER_ON[0],
            POWER_ON[1]
        )

        self._s.send(bytes(msg))
        self._s.recv(BUFFER_SIZE)

        self._disconnect()

    def power_off(self):

        self._connect()

        msg = self._assemble_cmd(
            POWER_OFF[0],
            POWER_OFF[1]
        )

        self._s.send(bytes(msg))
        self._s.recv(BUFFER_SIZE)

        self._disconnect()

    def get_model(self):
        self._connect()

        msg = self._assemble_cmd(
            GET_MODEL[0]
        )

        self._s.send(bytes(msg))
        data = self._s.recv(BUFFER_SIZE)

        if chr(data[4]) == 'A':
            print(chr(data[4]))

        print(hex(data[5]))
        print(hex(data[6]))
        print(hex(data[7]))
        print(hex(data[8]))
        print(hex(data[9]))

        self._disconnect()

    def get_serial(self):
        pass

    def get_temperature(self):

        self._connect()

        msg = self._assemble_cmd(
            SENSOR_LED_PLATE[0],
            SENSOR_LED_PLATE[1]
        )

        print(hex(msg[0]))
        print(hex(msg[1]))
        print(hex(msg[2]))
        print(hex(msg[3]))
        print(hex(msg[4]))
        print(hex(msg[5]))
        print("Sending")
        print()

        self._s.send(bytes(msg))

        data = self._s.recv(BUFFER_SIZE)

        self._disconnect()

        print(hex(data[0]))
        print(hex(data[1]))
        print(hex(data[2]))
        print(hex(data[3]))
        print(chr(data[4]))
        print(hex(data[5]))
        print(hex(data[6]))
        print(hex(data[7]))
