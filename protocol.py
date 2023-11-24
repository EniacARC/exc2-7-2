# struct(hton-int) + command + struct(hton-int) + params-binary
import logging
import socket
import struct

# define constants
MAX_PACKET = 1024
INT_SIZE = 4
PACK_SIGN = "I"


def receive_item(comm_socket):
    data_len = b''
    data = b''

    while len(data_len) < INT_SIZE:
        buf = comm_socket.recv(INT_SIZE - len(data_len))
        if buf == b'':
            data_len = b''
            break
        data_len += buf

    if data_len != b'':
        command_len = socket.htons(struct.unpack(PACK_SIGN, data_len)[0])

        while len(data) < command_len:
            buf = comm_socket.recv(command_len - len(data))
            if buf == b'':
                data = b''
                break
            data += buf

    return data


# send and receive funcs for the server that follow the established protocol
def receive(comm_socket):
    # command and data are binary
    # len command + command + len data + data
    command = b''
    data = b''
    buf = b''
    try:
        command = receive_item(comm_socket)
        if command != b'':
            data = receive_item(comm_socket)
    except socket.error as err:
        logging.error(f"error while trying to receive message from client: {err}")
        command = b''
        data = b''
    finally:
        return command, data if command != b'' and data != b'' else b'', b''


def send(comm_socket, command, data):
    # command and data are strings
    # len command + command + len data + data
    """
    sends the data, and it's length to the client. makes sure all the data was sent successfully

    :param: comm_socket
    :type: network socket
    :param: data
    :type: str
    :return: if the message was sent successfully: 0 for yes, 1 for no
    :rtype: int
    """
    return_code = 0
    command_len = struct.pack(PACK_SIGN, socket.htons(len(command)))
    data_len_net = struct.pack(PACK_SIGN, socket.htons(len(data)))
    to_send = command_len + command.encode() + data_len_net + data.encode()
    sent = 0
    try:
        # send message length
        while sent < len(to_send):
            sent += comm_socket.send(to_send[sent:])
    except socket.error as err:
        logging.error(f"error while trying to send message from client: {err}")
        # signal something went wrong
        return_code = 1
    return return_code
