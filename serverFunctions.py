"""
Author: Yonathan Chapal
Program name: Exc 2.7
Description: A basic commands server
Date: 24/11/2023
"""
import base64
import glob
import logging
import os
import shutil
import subprocess

from PIL import ImageGrab

# All functions return strings
# define constants
NO_PATH_ERROR = "no files found at path specified"
SUCCESS_MESSAGE = "COMMAND FINISHED SUCCESSFULLY"
ERROR_MESSAGE = "SOMETHING WENT WRONG"


def get_file_list(path):
    """
    Get a list of files in the specified path.

    :param path: The path to search for files.
    :type path: bytes

    :return: A string representation of the list of files or an error message.
    :rtype: str
    """
    # Convert path from binary string to string
    path = path.decode()
    # Ensure the path is in a valid format for glob search
    path = path.replace("/", "\\")
    files = glob.glob(rf"{path}/*.*", recursive=False)

    # Change format back to /
    files = list(map(lambda x: x.replace("\\", "/"), files))

    # Set the return value and log warning if no files were found
    str1 = ','.join(files) if len(files) > 0 else \
        logging.warning(f"no files found at path: '{path}'") or ERROR_MESSAGE + "WHILE LOOKING FOR FILES"
    return str1


def delete_file(path):
    """
    Delete a file at the specified path.

    :param path: The path of the file to be deleted.
    :type path: bytes

    :return: Success message if the deletion was successful, otherwise an error message.
    :rtype: str
    """
    return_value = SUCCESS_MESSAGE
    # Convert path from binary string to string
    path = path.decode()
    # Ensure the path is in a valid format for os.remove
    path = path.replace("/", "\\")
    try:
        os.remove(path)
        # Signal removal as successful
    except OSError as err:
        logging.error(f"error while trying to delete file at {path}: {err}")
        # Return error code
        return_value = ERROR_MESSAGE + "WHILE DELETING FILE"

    return return_value


def copy_file(src, dest):
    """
    Copy a file from source to destination.

    :param src: The source path of the file.
    :type src: bytes

    :param dest: The destination path for the copied file.
    :type dest: bytes

    :return: Success message if the copy was successful, otherwise an error message.
    :rtype: str
    """
    # Ensure the paths are using only /
    return_value = "COPY" + SUCCESS_MESSAGE
    # Convert paths from binary string to string
    src = src.decode()
    dest = dest.decode()
    # Ensure the path is in a valid format for shutil.copy
    src = src.replace("\\", "/")
    dest = dest.replace("\\", "/")
    try:
        shutil.copy(src, dest)
        # Signal copy as successful
    except OSError as err:
        logging.error(f"error while trying to copy file from {src} to {dest}: {err}")
        # Return error msg
        return_value = ERROR_MESSAGE + "WHILE COPYING FILE"

    return return_value


def execute_program(path):
    """
    Execute a program at the specified path.

    :param path: The path of the program to be executed.
    :type path: bytes

    :return: Success message if the execution was successful, otherwise an error message.
    :rtype: str
    """
    return_value = "EXECUTE" + SUCCESS_MESSAGE
    # Convert paths from binary string to string
    path = path.decode()
    # Ensure the path is using only / for subprocess.call
    path = path.replace("\\", "/")
    try:
        subprocess.call(path)
    except OSError as err:
        logging.error(f"os error while trying to execute program at {path}: {err}")
        return_value = ERROR_MESSAGE + "WHILE EXECUTING FILE"
    except subprocess.CalledProcessError as err:
        logging.error(f"program error while trying to execute program at {path}: {err}")
        return_value = ERROR_MESSAGE + "WHILE EXECUTING FILE"

    return return_value


def screenshot():
    """
    Capture a screenshot of all screens and save it as 'screenshot.jpg'.

    :return: Base64-encoded image if the screenshot was successful, otherwise an error message.
    :rtype: str
    """
    try:
        ImageGrab.grab(all_screens=True).save('screenshot.jpg')
        # call function to read photo
        with open('screenshot.jpg', 'rb') as img:
            return_value = base64.b64encode(img.read()).decode('utf-8')
    except OSError as err:
        logging.error(f"os error while trying to take a screenshot: {err}")
        # Return error code
        return_value = ''

    return return_value
