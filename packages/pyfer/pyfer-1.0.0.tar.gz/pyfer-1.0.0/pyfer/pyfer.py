"""
pyfer - Encrypt and Decrypt messages.

Classes
-------
Pyfer 
    
See class docstrings for class methods.
      
Module-Wide Functions
---------------------
generate_key
"""

import numpy as np
import string
import itertools

# ------------------------------------------------------------------------


def generate_key(key_length):

    """
    Generates a random string of digits of the specified length.
    """

    if type(key_length) is int:
        n = key_length
    else:
        raise Exception(
            f"key_length argument must be an integer; {type(key_length)} given."
        )

    str_key = "".join(
        ["{}".format(np.random.randint(0, 9)) for num in range(0, n)]
    )

    return str_key


# ------------------------------------------------------------------------


class Pyfer:

    """
    Class representing a Pyfer encryption object.

    Attributes
    ----------
    key (str): string of 12, 16, or 18 digits to serving as encryption
    key.
    -
    char_list (list) optional/dependent on init: list of characters used
    by the encryption object.
    -
    char_grid (numpy-array) optional/dependent on init: unscrambled grid
    version of list of characters used by the encryption object.
    -
    scramble_grid (numpy-array) optional/dependent on init: scrambled
    grid of characters to used for the encryption and decryption of
    messages.

    Methods
    -------
    init: constructs all the necessary attributes for the encryption
    object.
    -
    scramble: encrypts a message.
    -
    unscramble: decrypts a message.
    """

    def __init__(self, key):

        """
        Constructs all the necessary attributes for the encryption
        object.

        Works like a polybius square, excpet that the rows and columns
        of the grid are shuffled by the key prior to lookup.

        Arguments:
            key (str): string of 12, 16, or 18 digits to serving as
            encryption key.

        Returns:
            Pyfer encryption object.
        """

        lc_list = list(string.ascii_lowercase)
        uc_list = list(string.ascii_uppercase)
        d_list = list(string.digits)
        p_med = ["!", "?"]
        p_full = [
            "!",
            "?",
            ".",
            ",",
            ":",
            ";",
            ")",
            "(",
            "_",
            "+",
            "-",
            "=",
            "<",
            ">",
            "%",
            "*",
            "/",
            "$",
            "&",
        ]

        if type(key) is str:
            pass
        else:
            raise Exception(f"key must be a string; {type(key)} given.")

        if len(key) == 12:
            self.key = key
            self.char_list = [
                x
                for x in itertools.chain.from_iterable(
                    itertools.zip_longest(lc_list, d_list)
                )
                if x
            ]
        elif len(key) == 16:
            self.key = key
            self.char_list = [
                x
                for x in itertools.chain.from_iterable(
                    itertools.zip_longest(
                        lc_list, uc_list, d_list, p_med
                    )
                )
                if x
            ]
        elif len(key) == 18:
            self.key = key
            self.char_list = [
                x
                for x in itertools.chain.from_iterable(
                    itertools.zip_longest(
                        lc_list, uc_list, d_list, p_full
                    )
                )
                if x
            ]
        else:
            self.key = None
            self.char_list = None
            raise Exception(
                "Invalid key type: must be string of 12, 16, or 18 digits."
            )

        if self.key is not None:
            square = int(len(self.key) / 2)
            try:
                intkey = int(self.key)
            except:
                raise Exception(
                    "Invalid key type: must be string of 12, 16, or 18 digits."
                )
            finally:
                key_x_elements = []
                for i in self.key[0:square]:
                    key_x_elements.append(int(i))
                    x_key = np.argsort(np.array(key_x_elements))
                key_y_elements = []
                for i in self.key[(-1 * square) :]:
                    key_y_elements.append(int(i))
                    y_key = np.argsort(np.array(key_y_elements))

        self.char_grid = np.asarray(self.char_list).reshape(
            square, square
        )

        x_scramble_grid = self.char_grid[:, x_key]
        xy_scramble_grid = x_scramble_grid[y_key, :]

        self.scramble_grid = xy_scramble_grid

    #     ----------

    def scramble(self, input_string):

        """
        Scramble the input message using the Pyfer object.

        Arguments:
            input_string (str): message to encrypt.

        Returns:
            output_string (str): encrypted message.
        """

        if type(input_string) is str:
            if np.mod(len(input_string), 2) == 0:
                if len(input_string) > 1:
                    pass
                else:
                    raise Exception(
                        "Input string must have length greater than 1."
                    )
            else:
                raise Exception(
                    "Input string must have even number of characters and have length greater than 1."
                )
        else:
            raise Exception(
                "Input must be string of even length greater than 1."
            )

        in_indices = []
        for i in input_string:
            in_indices.append(np.argwhere(self.scramble_grid == i)[0])
        out_indices = np.reshape(
            np.transpose(np.array(in_indices)), (len(input_string), 2)
        )

        output_list = []
        for i in range(len(input_string)):
            output_list.append(
                self.scramble_grid[out_indices[i][0], out_indices[i][1]]
            )
        output_string = "".join(output_list)

        return output_string

    #     ----------

    def unscramble(self, input_string):

        """
        Unscramble the input message using the Pyfer object.

        Arguments:
            input_string (str): message to decrypt.

        Returns:
            output_string (str): decrypted message.
        """

        if type(input_string) is str:
            if np.mod(len(input_string), 2) == 0:
                if len(input_string) > 1:
                    pass
                else:
                    raise Exception(
                        "Input string must have length greater than 1."
                    )
            else:
                raise Exception(
                    "Input string must have even number of characters and have length greater than 1."
                )
        else:
            raise Exception(
                "Input must be string of even length greater than 1."
            )

        in_indices = []
        for i in input_string:
            in_indices.append(np.argwhere(self.scramble_grid == i)[0])
        out_indices = np.transpose(
            np.reshape(np.array(in_indices), (2, len(input_string)))
        )

        output_list = []
        for i in range(len(input_string)):
            output_list.append(
                self.scramble_grid[out_indices[i][0], out_indices[i][1]]
            )
        output_string = "".join(output_list)

        return output_string
