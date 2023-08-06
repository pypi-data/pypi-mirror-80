import logging
import threading
from typing import Union
from ftdi_serial import Serial
from prosonix.errors import SonolabError, SL10OverError
import atexit


class SL10:
    """
    Connection settings according to the manual are
    +----------------------+---------------------------------------------+
    | Parameter            | Comment                                     |
    +----------------------+---------------------------------------------+
    | Baud rate            | 9600                                        |
    +----------------------+---------------------------------------------+
    | Parity               | None                                        |
    +----------------------+---------------------------------------------+
    | Handshaking          | None                                        |
    +----------------------+---------------------------------------------+
    | Data bits            | 8                                           |
    +----------------------+---------------------------------------------+
    | Stop bits            | 1                                           |
    +----------------------+---------------------------------------------+
    | Physical connection  | Female RS232 9 way D type on SL10, connects |
    |                      | to PC via standard RS232 extension cable    |
    +----------------------+---------------------------------------------+
    | Message Terminators  | <CR> (for both send and receive)            |
    +----------------------+---------------------------------------------+

    Protocols are
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | Sent by PC | Response from SL10 | Parameter            | Description                                             |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | ON         | #ON                |                      | Switch system on                                        |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | OFF        | #OFF               |                      | Switch system off                                       |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | SPnnnn     | #SP                | nnnn is power, Watts | To set the ultrasonic power the command “SP”            |
    |            | (or #OVR if nnnn   |                      | should be used followed by the required power           |
    |            |                    |                      | setting in Watts.                                       |
    |            | is out of range)   |                      | nnnn is a floating point number in ASCII                |
    |            |                    |                      | format (e.g. 20.58).                                    |
    |            |                    |                      | If nnnn is out of range an #OVR response will be given  |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | GP         | #GPnnnn            | nnnn is power, Watts | To interrogate the system power setting the             |
    |            |                    |                      | “GP” command should be used and the generator           |
    |            |                    |                      | will return the power level.                            |
    |            |                    |                      | nnnn is a floating point number in ASCII                |
    |            |                    |                      | format (e.g. 20.58)                                     |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | LOC        | #LOC               |                      | Switch to local control of the system                   |
    +------------+--------------------+----------------------+---------------------------------------------------------+
    | REM        | #REM               |                      | Switch to remote control of the system. When operating  |
    |            |                    |                      | remotely the front panel controls are locked out. When  |
    |            |                    |                      | switching from local to remote to local settings        |
    |            |                    |                      | are maintained                                          |
    +------------+--------------------+----------------------+---------------------------------------------------------+

    """
    CONNECTION_SETTINGS = {'baudrate': 9600, 'data_bits': Serial.DATA_BITS_8, 'stop_bits': Serial.STOP_BITS_1}
    # hex command characters for data transmission
    CR_HEX = "\x0d"  # carriage return
    LINE_ENDING = CR_HEX  # each individual command and each response are terminated with CR
    LINE_ENDING_ENCODED = LINE_ENDING.encode()

    # constants for protocols and responses
    _ON = "ON"
    _OFF = 'OFF'
    _SET_POWER = 'SP'
    _READ_POWER = 'GP'
    _SET_TO_LOCAL = 'LOC'
    _SET_TO_REMOTE = 'REM'
    _OVER_ERROR = 'OVR'

    def __init__(self, device_port: str):
        self._device_port = device_port
        self.ser: Serial = None
        self._lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
        self.connect()

    @property
    def device_port(self) -> str:
        return self._device_port

    def connect(self):
        """Connect to the SL10 and switch to remote mode"""
        try:
            if self.ser is None:
                cn = Serial(device_port=self.device_port,
                            **self.CONNECTION_SETTINGS,
                            )
                self.ser = cn
            else:
                self.ser.connect()
            self.logger.debug('Connected to SL10')
            self.switch_to_remote()
            # Ensure that the serial port is closed on system exit
            atexit.register(self.disconnect)
        except Exception as e:
            self.logger.warning("Could not connect to an SL10, make sure the right port was selected")
            raise SonolabError("Could not connect to an SL10, make sure the right port was selected")

    def disconnect(self):
        """Disconnect from the SL10 and switch to local mode, doesnt turn it off"""
        if self.ser is None:
            # if SL10 is already disconnected then self.ser is None
            return
        try:
            self.switch_to_local()
            self.ser.disconnect()
            self.ser = None
            self.logger.debug('Disconnected from SL10')
        except Exception as e:
            self.switch_to_remote()
            self.logger.warning("Could not disconnect from SL10")

    def on(self) -> str:
        response = self._send_and_receive(self._ON)
        self.logger.debug('SL10 on')
        return response

    def off(self) -> str:
        response = self._send_and_receive(self._OFF)
        self.logger.debug('SL10 off')
        return response

    def power(self, value: float = None) -> Union[str, float]:
        """Set or read the current power. If no value is passed in,"""
        if value is None:  # check the power
            protocol = self._READ_POWER
        else:
            value = str(value)
            protocol = self._SET_POWER + value
        response = self._send_and_receive(protocol)
        if self._OVER_ERROR in response:
            raise SL10OverError(value)
        elif self._SET_POWER in response:
            self.logger.debug(f'SL10 power set to {value} Watts')
        elif self._READ_POWER in response:
            response = response[2:]
            response = float(response)
            self.logger.debug(f'SL10 power at {response} Watts')
        return response

    def switch_to_remote(self) -> str:
        response = self._send_and_receive(self._SET_TO_REMOTE)
        self.logger.debug(f'SL10 to remote control')
        return response

    def switch_to_local(self) -> str:
        response = self._send_and_receive(self._SET_TO_LOCAL)
        self.logger.debug(f'SL10 to local control')
        return response

    def _send_and_receive(self,
                          protocol: str,
                          ) -> str:
        """
        Send a protocol, get a response back, and return the response
        :param str, protocol: the string protocol to send to the SL10

        :return:
        """
        with self._lock:
            # format the command to send so that it terminates with the line ending (CR)
            formatted_command: str = protocol + self.LINE_ENDING
            formatted_command_encoded = formatted_command.encode()
            # this is the response, and the return string
            response_string = self.ser.request(data=formatted_command_encoded,
                                               line_ending=self.LINE_ENDING_ENCODED,
                                               ).decode()
            # remove the first character returned at the beginning of all responses, a hash (#)
            formatted_response = response_string[1:]
            return formatted_response
