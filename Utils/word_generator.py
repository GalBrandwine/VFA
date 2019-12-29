import DVFApy as dvfa_tool


def get_words():
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
