import abc
import socket
import struct
from array import array
from builtins import float
from typing import List

from Simis.Ashes import Model
from Simis.datastore import Listener

TCP_IP = 'localhost'
TCP_PORT = 6340


class TcpConnector(Listener, metaclass=abc.ABCMeta):
    """
    Class that manages a TCP connection to Python and that can send and receive data of a specified length
    """

    def __init__(self, answer_size: int, port: int = TCP_PORT, ip: str = TCP_IP, byte_swap: bool = True):
        """
        :param answer_size: Expected length of values returned to Python from TCP
        :param port: Port number, default: 6340
        :param ip: Ip of client, default: 'localhost'
        :param byte_swap: Specifies if Byte-swap is needed (True for Labview and Simulink)
        """
        super().__init__()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # type:socket

        # Disables Negler Algorithm and significantly speeds up a synchronous connection
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        s.bind((ip, port))
        print('Waiting for TCP connection')
        s.listen(1)
        self.conn, addr = s.accept()
        print('Connection address: ', addr)
        self.byte_swap = byte_swap  # type:bool
        self.answer_size = answer_size  # type:int
        self.output = []  # type:List[int]
        self.MSG_LEN = 0  # type:int
        self.set_answer_size(answer_size)
        self.last_time = -1  # type:int

    def set_answer_size(self, answer_size: int) -> None:
        """
        Sets the expected length of the values returned to Python from TCP.
        :param answer_size: The expected length
        """
        self.answer_size = answer_size
        self.output = [0] * self.answer_size
        self.MSG_LEN = 8 * self.answer_size

    def get_last_return_value(self) -> List[float]:
        """
        :return: the last received value list
        """
        return self.output

    def send_and_receive(self, values: List[float]) -> List[float]:
        """
        Send the specified list of values over tcp and waits for a response of the size given in the constructor (answer_size)
        :param values: The values to send
        :return: List received from TCP
        """
        # Send data
        for value in values:
            if self.byte_swap:
                # Byte-swap data if needed
                msg = struct.pack('>d', value)
            else:
                msg = struct.pack('<d', value)
            self.conn.send(msg)
        data = b''

        # Receive data
        while len(data) < self.MSG_LEN:
            chunk = self.conn.recv(self.MSG_LEN - len(data))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            data = data + chunk
        try:
            ret_values = array('d', data)
            if self.byte_swap:
                ret_values.byteswap()
        except ValueError as e:
            print(e)
            ret_values = [0] * self.answer_size

        self.output = ret_values
        return self.output

    def notify(self, model: Model) -> None:
        # Check if time already called before, if yes then just return
        t = model.time
        d = t - self.last_time
        if not d:
            return
        # Call user-defined method to extract the values from the Ashes model
        l = self.process_input(model)
        retval = self.send_and_receive(l)
        # Call user-defined method to write the returned values from TCP into the Ashes model that will be written out.
        self.process_output(model, retval)
        self.last_time = t

    @abc.abstractmethod
    def process_input(self, model: Model) -> List[float]:
        """
        This method should process the input to the TCP connection. This means it should extract the wanted values from
        the model that is provided by Ashes and put them into a list for sending over TCP
        :param model: The model provided by Ashes
        :return: The list of values to send over TCP
        """
        print("METHOD IS ABSTRACT AND NOT IMPLEMENTED IN BASECLASS")

    @abc.abstractmethod
    def process_output(self, model: Model, values: List[float]) -> None:
        """
        This method should process the values returned by the TCP connection and put them into the model structure so
        that they can be sent to Ashes.
        :param model: The model that will be sent to Ashes
        :param values: The values returned by the TCP connection
        """
        print("METHOD IS ABSTRACT AND NOT IMPLEMENTED IN BASECLASS")
