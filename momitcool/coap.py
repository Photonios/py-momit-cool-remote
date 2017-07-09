import sys
import socket
import struct
import logging

from enum import Enum
from random import randint
from typing import List

LOGGER = logging.getLogger(__name__)

COAP_DEFAULT_PORT = 5683


class CoapCode(Enum):
    """Enumuration of available CoAP codes."""

    PUT = 3


class CoapOptionCode(Enum):
    """Enumuration of codes for CoAP options."""

    URI_PATH = 0xb5
    URI_PATH_SEPARATOR = 0x01
    CONTENT_FORMAT = 0x12
    END = 0xff


class CoapOptions:
    """CoAP request options."""

    path = []
    content_format = None

    def __init__(self, **kwargs):
        """Initializes a new instance of the :see:CoapOptions
        class with the specified set of options."""

        for key, value in kwargs.items():
            setattr(self, key, value)

    def encode(self):
        """Encodes this set of options."""

        options_buffer = b''

        if self.path and len(self.path) > 0:
            options_buffer += struct.pack('B', CoapOptionCode.URI_PATH.value)
            for index, path in enumerate(self.path):
                options_buffer += path.encode()

                # no trailing separator
                if index != len(self.path) - 1:
                    options_buffer += struct.pack('B', CoapOptionCode.URI_PATH_SEPARATOR.value)

        if self.content_format:
            options_buffer += struct.pack('B', CoapOptionCode.CONTENT_FORMAT.value)
            options_buffer += struct.pack('!H', self.content_format)

        options_buffer += struct.pack('B', CoapOptionCode.END.value)
        return options_buffer


class CoapMessage:
    """A CoAP message."""

    host = 'localhost'
    port = COAP_DEFAULT_PORT
    code = CoapCode.PUT
    options = CoapOptions()
    payload = b''

    def __init__(self, **kwargs):
        """Initializes a new instance of the :see:CoapMessage class."""

        for key, value in kwargs.items():
            setattr(self, key, value)

    def encode(self):
        """Encodes the message into a binary structure that can
        be send over the wire."""

        message_id = randint(0x0, 0xffff) # maximum value of ushrt
        token = struct.pack('I', randint(0, 0xffffffff)) # maxmium value of uint

        request_buffer = b'\x44'
        request_buffer += struct.pack('B', self.code.value)
        request_buffer += struct.pack('H', randint(0x0, message_id))
        request_buffer += token
        request_buffer += self.options.encode()
        request_buffer += self.payload

        return request_buffer

    def send(self):
        """Sends the message to the configured destination."""

        packet = self.encode()
        LOGGER.debug('%s coap://%s:%s/%s (%d bytes)\n\n' \
                     '%s',
                     self.code.name, self.host, self.port,
                     '/'.join(self.options.path), len(packet),
                     str(self.payload))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', COAP_DEFAULT_PORT))
        sock.sendto(packet, (self.host, self.port))
