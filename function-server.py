import base64
import glob
import logging
import os
import shutil
import subprocess

from PIL import ImageGrab

# define constants
NO_PATH_ERROR = "no files found at path specified"


def get_file_list(path):
    # Convert path from binary string to string
    path = path.decode()
    # Ensure the path is in a valid format for glob search
    path = path.replace("/", "\\")
    files = glob.glob(rf"{path}/*.*", recursive=False)

    # Change format back to /
    files = list(map(lambda x: x.replace("\\", "/"), files))

    # Set the return value and log warning if no files were found
    str1 = str(files) if len(files) > 0 else logging.warning(f"no files found at path: '{path}'") or NO_PATH_ERROR
    return str1


def delete_file(path):
    return_code = 0
    # Ensure the path is using only /
    path = path.replace("\\", "/")
    try:
        os.remove(path)
        # Signal removal as successful
    except OSError as err:
        logging.error(f"error while trying to delete file at {path}: {err}")
        # Return error code
        return_code = "ERROR"

    return return_code


def copy_file(src, dest):
    """
    Copy a file from source to destination.

    :param src: The source path of the file.
    :type src: str

    :param dest: The destination path for the copied file.
    :type dest: str

    :return: 0 if successful, error code otherwise.
    :rtype: int
    """
    return_code = 0
    # Ensure the paths are using only /
    src = src.replace("\\", "/")
    dest = dest.replace("\\", "/")
    try:
        shutil.copy(src, dest)
        # Signal copy as successful
    except OSError as err:
        logging.error(f"error while trying to copy file from {src} to {dest}: {err}")
        # Return error code
        return_code = err.args[0]

    return return_code


def execute_program(path):
    """
    Execute a program at the specified path.

    :param path: The path of the program to be executed.
    :type path: str

    :return: 0 if successful, error code otherwise.
    :rtype: int
    """
    return_code = 0
    # Ensure the path is using only /
    path = path.replace("\\", "/")
    try:
        subprocess.call(path)
    except OSError as err:
        logging.error(f"os error while trying to execute program at {path}: {err}")
        return_code = err.args[0]
    except subprocess.CalledProcessError as err:
        logging.error(f"program error while trying to execute program at {path}: {err}")
        return_code = err.args[0]

    return return_code


def screenshot():
    """
    Capture a screenshot of all screens and save it as 'screenshot.jpg'.

    :return: 0 if successful, error code otherwise.
    :rtype: int
    """
    return_value = None
    try:
        ImageGrab.grab(all_screens=True).save('screenshot.jpg')
        # call function to read photo
        base64_bytes = b''
        with open('screenshot.jpg', 'rb') as img:
            base64_bytes = base64.b64encode(img.read()).decode('utf-8')
        return base64_bytes
    except OSError as err:
        logging.error(f"os error while trying to take a screenshot: {err}")
        # Return error code
        return_value = None

    return return_value
