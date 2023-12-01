import base64
import binascii
import logging
from io import BytesIO

from PIL import Image

STRING_START = "Server responded:"


def decode_image(base64_bytes):
    """
    Decode a base64-encoded image, save it to a file, and show it.

    :param base64_bytes: The base64-encoded image data.
    :type base64_bytes: bytes

    :return: None
    """
    try:
        base64str = base64_bytes.decode()
        # Decode the base64 string back to image data
        decoded_image = base64.b64decode(base64str)

        # Create a PIL Image object from the decoded image data
        image = Image.open(BytesIO(decoded_image))
        image.save('output_image.jpg')
        image.show()
    except binascii.Error as err:
        logging.error(f"eror while trying to decode image! '{err}'")
        print(f"Error decoding base64: {err}")


def decode_path(arr):
    """
    Decode and format a path represented as a byte array.

    :param arr: The byte array representing the path.
    :type arr: bytes

    Prints the formatted path to the console.
    """
    my_list = arr.decode().split("|")
    print(STRING_START)
    formatted_list = "\n".join(my_list)
    print(formatted_list)


def general_out(data):
    """
    Print general output information.

    :param data: The data to be printed.
    :type data: bytes

    Prints formatted output information to the console.
    """
    print(f"{STRING_START} {data.decode()}")