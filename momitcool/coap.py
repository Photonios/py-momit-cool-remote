import sys
import socket
import struct
import logging

from enum import Enum
from random import randint
from typing import List

LOGGER = logging.getLogger(__name__)

COAP_BUFFER_SIZE = 1024
COAP_DEFAULT_PORT = 5683


class CoapBuffer:
    """Helps in reading from a data stream."""

    def __init__(self, data=None, offset=0):
        self.data = data or bytes()
        self.offset = offset or 0

    def read(self, count=None, peek=False):
        if count is None:
            count = len(self.data) - self.offset

        data = self.data[self.offset:self.offset + count]
        if not peek:
            self.offset += count

        return data

    @staticmethod
    def unpack(data_type, data):
        if len(data) == 0:
            return None
        return struct.unpack(data_type, data)[0]

    def read_byte(self, peek=False):
        return self.unpack('B', self.read(1, peek))

    def read_ushort(self, peek=False):
        return self.unpack('H', self.read(2, peek))

    def read_uint(self, peek=False):
        return self.unpack('I', self.read(4, peek))


class CoapCode(Enum):
    """Enumuration of available CoAP codes."""

    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    CHANGED = 68
    CONTENT = 69
    NOT_FOUND = 132


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
        token = randint(0, 0xffffffff) # maximum value of uint

        request_buffer = b'\x44'
        request_buffer += struct.pack('B', self.code.value)
        request_buffer += struct.pack('H', message_id)
        request_buffer += struct.pack('I', token)
        request_buffer += self.options.encode()
        request_buffer += self.payload

        return request_buffer

    @staticmethod
    def decode(data):
        """Decodes a message in a binary structure."""

        # first byte is version etc, we don't care
        buffer = CoapBuffer(data, offset=1)

        code = buffer.read_byte()
        message_id = buffer.read_ushort()
        token = buffer.read_uint()


        # don't read options for now, just read the size, and swallow
        # the option values so we can get to the payload
        end_reached = lambda data: data == CoapOptionCode.END.value or data is None
        while not end_reached(buffer.read_byte(peek=True)):
            option_length = buffer.read_byte() & 0xF
            buffer.read(option_length)

        # swallow the options END marker
        buffer.read_byte()

        return CoapMessage(
            code=CoapCode(code),
            message_id=message_id,
            token=token,
            payload=buffer.read()
        )

    def send(self):
        """Sends the message to the configured destination."""

        packet = self.encode()
        LOGGER.debug('%s coap://%s:%s/%s (%d bytes)\n\n' \
                     '>> %s',
                     self.code.name, self.host, self.port,
                     '/'.join(self.options.path), len(packet),
                     str(self.payload))

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('0.0.0.0', COAP_DEFAULT_PORT))
        sock.sendto(packet, (self.host, self.port))

        data, addr = sock.recvfrom(COAP_BUFFER_SIZE)
        message = CoapMessage.decode(data)

        LOGGER.debug('%s coap://%s:%s (%d bytes)\n\n' \
                     '<< %s',
                     message.code.name, addr[0], addr[1],
                     len(message.payload), str(message.payload))

        return message
