"""
Author: Yonathan Chapal
Program name: Exc 2.7
Description: A basic commands server
Date: 24/11/2023
"""
import binascii
import sys

from protocol import *
from serverFunctions import *
import stat

# define network constants
LISTEN_IP = '0.0.0.0'
LISTEN_PORT = 17207
Q_LEN = 1
MAX_PACKET = 1024
COMMANDS = {"DIR": get_file_list.__call__, "DELETE": delete_file.__call__, "COPY": copy_file.__call__,
            "EXECUTE": execute_program.__call__, "TAKE SCREENSHOT": screenshot.__call__}

# Assert constants
PROGRAM_DIR = os.getcwd()
PARENT_DIR = PROGRAM_DIR + '\\autotest\\'
EXEC_ASSERT = PROGRAM_DIR + "\\simple_script.exe"
SUCCESS_ID = "SUCCESSFUL"
FILE1 = "file1.txt"
FILE2 = "file2.txt"
FILE_CONTENTS = "Hello I Am File1!"
JPG_MAGIC_NUMS = b'\xff\xd8\xff\xe0'

# define log constants
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/loggerServer.log'


# remove directory with read-only files
def rm_dir_readonly(func, path, _):
    """
    Clear the readonly bit and reattempt the removal

    :param func: The function responsible for removing the directory.
    :type func: typing.Callable

    :param path: The path of the directory to be removed.
    :type path: str

    :param _: Ignored parameter (used by shutil.rmtree).
    :type _: object

    :return: None
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def ready_server(server_socket):
    """
    binds the server and puts it in listen mode
    :param server_socket: the socket of the server
    :type server_socket: socket.socket
    :return: None
    """
    server_socket.bind((LISTEN_IP, LISTEN_PORT))
    logging.debug(f"socket bound: ({LISTEN_IP} : {LISTEN_PORT})")
    server_socket.listen(Q_LEN)
    logging.debug(f"server is listening and is ready to accept {Q_LEN} connections")


def connect_a_client(server_socket):
    logging.debug("waiting for incoming connection...")
    client, addr = server_socket.accept()
    logging.debug("connection established")
    return client, addr


def do_command(client_socket, command, payload):
    """
    Execute a specified command based on the given command string.

    :param client_socket: The client socket to communicate with.
    :type client_socket: socket.socket

    :param command: The command to be executed.
    :type command: str

    :param payload: the command parameters.
    :type payload: bytes

    :return: Return code(0 if successful, 1 if there's a send error, 2 to close connection)
    :rtype: int
    """
    if command != '':
        if command in COMMANDS.keys():
            logging.debug(f"executing: {COMMANDS[command]}()")
            res = COMMANDS[command](payload)
        elif command == "EXIT":
            logging.debug("client wants to terminate session")
            res = "GOODBYE"
            r_code = 2
        else:
            logging.warning(f"unknown command!: {command}")
            res = "UNKNOWN COMMAND"

        logging.info(f"server sending: {res}")
        r_code = send(client_socket, command, res)
    else:
        logging.error("connection with client was terminated!")
        r_code = 2

    return r_code


def handle_a_client(client_socket):
    disconnect = False
    try:
        while not disconnect:
            command, payload = receive(client_socket)
            logging.debug(f"{command}, {payload}")
            r_code = do_command(client_socket, command, payload)
            disconnect = False if r_code == 0 else True
    except socket.error as err:
        logging.error(f"error involving the client socket detected!: {err}")
    except KeyboardInterrupt:
        print("How U Doin'?")
    finally:
        client_socket.close()
        logging.debug("closed client socket")

    return disconnect


def address_a_client(server_socket):
    """
    used to handle 1 client
    :param server_socket: the socket of the server
    :type: socket.socket
    :return: -
    """
    connected = True
    while connected:
        client_socket, client_addr = connect_a_client(server_socket)
        connected = handle_a_client(client_socket)


def main():
    # define an ipv4 tcp socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ready_server(server_socket)
        address_a_client(server_socket)
    except socket.error as err:
        logging.error(f"error involving the server socket detected!: {err}")


if __name__ == "__main__":
    # make sure we have a logging directory and configure the logging
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # assert program
    # Create the folder for assert testing
    if os.path.isdir(PARENT_DIR):
        shutil.rmtree(PARENT_DIR, onerror=rm_dir_readonly)
    os.mkdir(PARENT_DIR)
    try:
        with open((PARENT_DIR + FILE1), "w") as f:
            f.write(FILE_CONTENTS)

        result = copy_file((PARENT_DIR + FILE1 + "|" + PARENT_DIR + FILE2).encode())
        assert SUCCESS_ID in result

        with open((PARENT_DIR + FILE2), "r") as f:
            assert f.read() == FILE_CONTENTS

        result = get_file_list(PARENT_DIR.encode())
        assert len(result.split('|')) == 2 and FILE1 in result and FILE2 in result

        # the script executed writes over the contents of file2.txt to 'EXECUTED'
        assert SUCCESS_ID in execute_program(EXEC_ASSERT.encode())

        with open((PARENT_DIR + FILE2), "r") as f:
            assert f.read() == "EXECUTED"

        assert SUCCESS_ID in delete_file((PARENT_DIR + FILE2).encode())
        result = get_file_list(PARENT_DIR.encode())
        assert len(result.split('|')) == 1 and FILE1 in result

        # Assert screenshot func returns a non-empty jpg image
        result = base64.b64decode(screenshot(b''))
        assert result != ''
        assert result[:4] == JPG_MAGIC_NUMS
        main()
    except (OSError, binascii.Error,):
        raise AssertionError("something went wrong")