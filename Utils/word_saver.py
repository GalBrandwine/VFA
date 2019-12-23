import numpy
from DVFApy.word import Word


def save(word: Word, path: str, word_name: str):
    one_line = numpy.asarray([word.word])
    has_csv_tail = word_name.find("csv")
    if has_csv_tail < 0:
        numpy.savetxt("{}/{}.csv".format(path, word_name), one_line, delimiter=",")
    else:
        numpy.savetxt("{}/{}".format(path, word_name), one_line, delimiter=",")

# Test
if __name__ == "__main__":
    import os
    word = Word([1,2,3])
    cwd = os.getcwd()
    print(cwd)
    save(word,cwd, "temp_word")
