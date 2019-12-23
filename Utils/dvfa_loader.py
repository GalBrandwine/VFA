from DVFApy.dvfa import DVFA
import pickle


def load(path_to_dvfa: str) -> DVFA:
    infile = open(path_to_dvfa, 'rb')
    dvfa = pickle.load(infile)
    infile.close()
    return dvfa


if __name__ == "__main__":
    import os

    cwd = os.getcwd()
    print(cwd)
    ret = load(cwd + "/" + "x1_x1.pickle")
    print(ret)
