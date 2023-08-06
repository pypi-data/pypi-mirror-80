"""

Source code for text code generator

@creator -> LokotamaTheMastermind
@email -> lokotamathemastermind2@gmail.com
@created -> 3/8/2020
@license -> MIT
@categories -> helpers, handlers, python, pip, text code generator
@supported -> [>=python3]
@contributors -> [LokotamaTheMastermind]

"""

import random_string as string
import url64
import random


def generate(length_minimal=10, length_maximal=15, int_min_length=9999, int_max_length=9999999):
    """ Generates text code
    Params:
        length_minimal (int): minimal----length
        length_maximal (int): maximal ---- length
        int_min_length (int): minimal ---- number
        int_max_length (int): maximal ----- number
    """
    code_type = random.choice(
        ['Alphabets', 'Numbers', 'Both'])  # Selects code type
    if code_type == "Alphabets":
        final = string.generate(
            length_minimal, length_maximal)  # Stage 1 -> string
        return final
    elif code_type == "Numbers":
        stage1 = string.generate(
            length_minimal, length_maximal, alphabet='1234567890')  # Stage 1 -> string
        final = f"{stage1}"  # Final -> stage1 + stage2
        return final
    elif code_type == "Both":
        stage1 = string.generate(
            length_minimal, length_maximal)  # Stage 1 -> string
        stage2 = random.randint(
            int_min_length, int_max_length)  # Stage 2 -> int
        # Stage3 -> string + int = large_string
        stage3 = f"{stage1}{stage2}"
        final = url64.encode(stage3)  # Final -> Encoded <- stage3
        return final
