"""
Author: Yonathan Chapal
Program name: Exc 2.7
Description: A basic commands server
Date: 24/11/2023
"""
# struct(hton-int) + command + struct(hton-int) + params-binary
import logging
import socket
import struct

# define constants
MAX_PACKET = 1024
INT_SIZE = 4
PACK_SIGN = "I"


def receive_item(comm_socket):
    """
    Receive a length-data pair that is part of the message from the communication socket.

    :param comm_socket: The communication socket.
    :type comm_socket: socket.socket

    :return: The received data.
    :rtype: bytes
    """
    data_len = b''
    data = b''

    while len(data_len) < INT_SIZE:
        buf = comm_socket.recv(INT_SIZE - len(data_len))
        if buf == b'':
            data_len = b''
            break
        data_len += buf

    if data_len != b'':
        command_len = socket.htonl(struct.unpack(PACK_SIGN, data_len)[0])

        while len(data) < command_len:
            buf = comm_socket.recv(command_len - len(data))
            if buf == b'':
                data = b''
                break
            data += buf

    return data


# send and receive funcs for the server that follow the established protocol
def receive(comm_socket):
    """
    Receive a message from the communication socket using the established protocol.

    :param comm_socket: The communication socket.
    :type comm_socket: socket.socket

    :return: Tuple containing command and data parts of the message.
    :rtype: tuple[str, bytes]
    """
    command = b''
    data = b''
    buf = b''
    try:
        command = receive_item(comm_socket)
        if command != b'':
            data = receive_item(comm_socket)
    except socket.error as err:
        logging.error(f"error while trying to receive message: {err}")
        command = b''
        data = b''
    finally:
        return command.decode(), data


def send(comm_socket, command, data):
    """
    Send a message over the communication socket using the established protocol.

    :param comm_socket: The communication socket.
    :type comm_socket: socket.socket

    :param command: The command part of the message.
    :type command: str

    :param data: The data part of the message.
    :type data: str

    :return: Return code (0 if successful, 1 if there's an error).
    :rtype: int
    """
    return_code = 0
    command_len = struct.pack(PACK_SIGN, socket.htonl(len(command)))
    data_len_net = struct.pack(PACK_SIGN, socket.htonl(len(data)))
    to_send = command_len + command.encode() + data_len_net + data.encode()
    sent = 0
    try:
        # send message length
        while sent < len(to_send):
            sent += comm_socket.send(to_send[sent:])
    except socket.error as err:
        logging.error(f"error while trying to send message: {err}")
        # signal something went wrong
        return_code = 1
    return return_code
