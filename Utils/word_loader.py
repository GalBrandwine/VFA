import numpy
from DVFApy.word import Word


def load(path: str) -> Word:
    loaded = numpy.genfromtxt(path, delimiter=',')
    return Word(loaded)


# Test
if __name__ == "__main__":
    import os
    word = Word([1,2,3])
    cwd = os.getcwd()
    ret = load(cwd + "/" + "temp_word.csv")
    print(ret)
