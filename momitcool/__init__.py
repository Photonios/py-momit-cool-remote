from .coap import CoapMessage


class MomitCool:
    """Represents a single MomitCool device."""

    def __init__(self, host: str, port: int):
        """Initializes a new instance of the :see:MomitCool class
        with the specified host and port."""

        self.host = host
        self.port = port

    def on(self):
        """Turns on the air-conditioning."""

        message = CoapMessage(host=self.host, port=self.port)
        message.options.path = ['10242', '0', '0']
        message.options.content_format = 1541
        message.payload = b'cm=cool,t=472,sp=200'
        message.send()

    def off(self):
        """Turns off the air-conditioning."""

        message = CoapMessage(host=self.host, port=self.port)
        message.options.path = ['10242', '0', '0']
        message.options.content_format = 1541
        message.payload = b'cm=cool,t=0,sp=off'
        message.send()
