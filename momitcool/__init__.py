import socket
import logging

from enum import Enum

from .coap import CoapMessage, CoapCode

LOGGER = logging.getLogger(__name__)


class MomitCoolMode(Enum):
    COOL = 'cool'
    HEAT = 'heat'
    OFF = 'off'
    UNKNOWN = '?'


class MomitCool:
    """Represents a single MomitCool device."""

    def __init__(self, host: str):
        """Initializes a new instance of the :see:MomitCool class
        with the specified host."""

        self.host = host
        self.port = 17062

    def mode(self):
        """Gets whether the air-conditioning mode."""

        message = CoapMessage(host=self.host, port=self.port, code=CoapCode.GET)
        message.options.path = ['10242', '0', '0']
        message.options.content_format = 1541
        response = message.send()

        parameters = self._decode_parameters(response.payload)
        return MomitCoolMode(parameters.get('out'))

    def temperature(self):
        message = CoapMessage(host=self.host, port=self.port, code=CoapCode.GET)
        message.options.path = ['10241', '0', '0']
        message.options.content_format = 1541
        response = message.send()

        temperature, _ = response.payload.decode().split(',', 1)
        return int(temperature) / 10

    def cool(self):
        """Turns on the air-conditioning in cooling mode."""

        LOGGER.info('Turning on air-conditioning in cooling mode')

        params = (
            ('cm', 'cool'), # mode: 'cool' or 'heat'
            ('t', '1440'), # time till turn off in minutes, 24 hours
            ('sp', '15'), # target temperature, 290 = 29.0C
        )

        message = CoapMessage(host=self.host, port=self.port)
        message.options.path = ['10242', '0', '0']
        message.options.content_format = 1541
        message.payload = self._encode_parameters(params)
        message.send()

    def off(self):
        """Turns off the air-conditioning."""

        LOGGER.info('Turning off air-conditioning')

        params = (
            ('cm', 'cool'),
            ('t', '0'),
            ('sp', 'off')
        )

        message = CoapMessage(host=self.host, port=self.port)
        message.options.path = ['10242', '0', '0']
        message.options.content_format = 1541
        message.payload = self._encode_parameters(params)
        message.send()

    def _encode_parameters(self, parameters: dict):
        """Encodes the payload parameters for transmission."""

        result = ','.join([
            '%s=%s' % (key, value)
            for key, value in parameters
        ])

        return result.encode()

    def _decode_parameters(self, payload):
        """Decodes parameters from a message."""

        parameters = dict()
        pairs = payload.decode().split(',')

        for pair in pairs:
            key, value = pair.split('=', 2)
            parameters[key] = value

        return parameters
