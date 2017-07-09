import logging

from .coap import CoapMessage

LOGGER = logging.getLogger(__name__)


class MomitCool:
    """Represents a single MomitCool device."""

    def __init__(self, host: str, port: int=19924):
        """Initializes a new instance of the :see:MomitCool class
        with the specified host and port."""

        self.host = host
        self.port = port

    def on(self):
        """Turns on the air-conditioning."""

        LOGGER.info('Turning on air-conditioning')

        params = (
            ('cm', 'cool'), # mode: 'cool' or 'heat'
            ('t', '1440'), # time till turn off in minutes, 24 hours
            ('sp', '0'), # target temperature, 290 = 29.0C
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
