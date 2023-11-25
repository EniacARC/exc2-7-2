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

# Assert constants
PROGRAM_DIR = os.getcwd()
PARENT_DIR = PROGRAM_DIR + '\\autotest\\'
EXEC_ASSERT = PROGRAM_DIR + "\\simple_script.exe"
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


def main():
    print("hello world")


if __name__ == "__main__":
    # make sure we have a logging directory and configure the logging
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
    logging.basicConfig(format=LOG_FORMAT, filename=LOG_FILE, level=LOG_LEVEL)

    # assert program
    # Create the folder for assert testing
    os.mkdir(PARENT_DIR)
    try:
        with open((PARENT_DIR + FILE1), "w") as f:
            f.write(FILE_CONTENTS)

        result = copy_file((PARENT_DIR + FILE1).encode(), (PARENT_DIR + FILE2).encode())
        assert "SUCCESSFUL" in result

        with open((PARENT_DIR + FILE2), "r") as f:
            assert f.read() == FILE_CONTENTS

        result = get_file_list(PARENT_DIR.encode())
        assert len(result.split('|')) == 2 and FILE1 in result and FILE2 in result

        # the script executed writes over the contents of file2.txt to 'EXECUTED'
        assert "SUCCESSFUL" in execute_program(EXEC_ASSERT.encode())

        with open((PARENT_DIR + FILE2), "r") as f:
            assert f.read() == "EXECUTED"

        assert "SUCCESSFUL" in delete_file((PARENT_DIR + FILE2).encode())
        result = get_file_list(PARENT_DIR.encode())
        assert len(result.split('|')) == 1 and FILE1 in result

        # Assert screenshot func returns a non-empty jpg image
        result = base64.b64decode(screenshot())
        assert result != ''
        assert result[:4] == JPG_MAGIC_NUMS

        main()
    except (OSError, binascii.Error,):
        raise AssertionError("something went wrong")
    finally:
        shutil.rmtree(PARENT_DIR, onerror=rm_dir_readonly)
