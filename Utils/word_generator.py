import numpy as np

import DVFApy as dvfa_tool


def palin_generator(n_input: int) -> list:
    """Generates all palindromes with lengt of n_input.

    WARNING: super inefficient!
    """
    max_len = 1000000
    str_len = len(str(max_len))

    if n_input >= str_len:
        message = "Input must be smaller than: {}".format(len(str(max_len)))
        raise Exception(message)

    palindromes = []

    for count in range(max_len):
        n = str(count)
        if n == n[::-1]:
            palindromes.append(n)

    return [pal for pal in palindromes if (len(pal) == n_input)]


def get_pal3_word() -> dvfa_tool.word.Word:
    first_letter = np.random.randint(500)
    second_letter = np.random.randint(500)
    third_letter = first_letter
    letters = [first_letter, second_letter, third_letter]
    return dvfa_tool.word.Word(letters)


def get_words() -> dvfa_tool.word.Word:
    arr_list = [
        [1, 2, 1],
        [1, 1, 1],
        [1, 2],
        [1, 2, 2],
        [1, 2, 3, 2, 2, 1],
        [1, 2, 3, 4, 5, 6],
        [0, 1, 0, 1],
        [99, 1, 99],
        [1, 3, 5, 7, 9, 11],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [56, 44, 58, 44, 213]
    ]

    word_list = []
    for arr in arr_list:
        word_list.append(dvfa_tool.word.Word(arr))
    return word_list
