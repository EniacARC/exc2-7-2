"""
Author: Yonathan Chapal
Program name: Exc 2.7
Description: A basic commands server
Date: 24/11/2023
"""
import base64
import binascii
import logging
import os
import socket
from io import BytesIO
from PIL import Image
from protocol import *
from clientFunctions import *

# define network constants
SERVER_IP = '127.0.0.1'
SERVER_PORT = 17207
Q_LEN = 1
MAX_PACKET = 1024
COMMAND_LEN = 4
HEADER_LEN = 2
STOP_SERVER_CONNECTION = "EXIT"
PHOTO_COMMAND = "TAKE SCREENSHOT"
SHOW_COMMAND = "SHOW COMMANDS"
ERR_INPUT = "ERROR! unknown command!"
COMMANDS = {"DIR": (1, decode_path.__call__), "DELETE": (1, general_out.__call__),
            "COPY": (2, general_out.__call__), "EXECUTE": (1, general_out.__call__),
            "TAKE SCREENSHOT": (0, decode_image.__call__), "EXIT": (0, general_out.__call__)}
VALID_COMMANDS = f"valid commands: |{'|'.join(COMMANDS)}|" + ' - {' + SHOW_COMMAND + '}'

# define log constants
LOG_FORMAT = '%(levelname)s | %(asctime)s | %(processName)s | %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_DIR = 'log'
LOG_FILE = LOG_DIR + '/loggerClient.log'


def main():
    # define an ipv4 tcp socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        logging.info(f"trying to connect to server at ({SERVER_IP}, {SERVER_PORT})")
        client.connect((SERVER_IP, SERVER_PORT))

        print(VALID_COMMANDS)
        want_to_exit = False
        while not want_to_exit:
            try:
                args = ''
                command = input("Enter command:").upper()

                if command == SHOW_COMMAND:
                    print(VALID_COMMANDS)
                elif command in COMMANDS.keys():
                    if COMMANDS[command] != 0:
                        args = [input(f"Enter arg: ") for _ in range(COMMANDS[command][0])]
                        args = "|".join(args)
                    send(client, command, args)
                    command, res = receive(client)
                    if command in COMMANDS.keys():
                        COMMANDS[command][1](res)
                    else:
                        print(res)
                else:
                    print(ERR_INPUT)

                if command == "EXIT":
                    want_to_exit = True
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                want_to_exit = True
    except socket.error as err:
        print(err)
    finally:
        client.close()


if __name__ == "__main__":
    # make sure we have a logging directory and configure the logging
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    main()
