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
)

_LOGGER = logging.getLogger(__name__)


class MDC:
    """ Multiple Display Control class """

    def __init__(self, host, port=1515, unit_id=0x00):

        self._host = host
        self._port = int(port)
        self._id = unit_id

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((self._host, self._port))

    def _calculate_checksum(self, data):
        return sum(data) % 256

    def _parse_response(data):
        pass

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
        msg = self._assemble_cmd(GET_VOLUME[0])

        self._s.send(bytes(msg))
        data = self._s.recv(BUFFER_SIZE)

        self._s.close()

        return(data)

    def power_status(self):
        msg = self._assemble_cmd(
            POWER_STATUS[0]
        )

        self._s.send(bytes(msg))

        data = self._s.recv(BUFFER_SIZE)

        if chr(data[4]) == 'A':
            if data[6]:
                return "Powered on"
            else:
                return "Powered off"

    def power_on(self):

        msg = self._assemble_cmd(
            POWER_ON[0],
            POWER_ON[1]
        )

        self._s.send(bytes(msg))
        self._s.recv(BUFFER_SIZE)

    def power_off(self):

        msg = self._assemble_cmd(
            POWER_OFF[0],
            POWER_OFF[1]
        )

        self._s.send(bytes(msg))
        self._s.recv(BUFFER_SIZE)
