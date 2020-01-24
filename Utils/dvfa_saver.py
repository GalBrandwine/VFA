import pickle

from DVFApy.dvfa import DVFA


def save(dvfa: DVFA, path: str, dvfa_name: str):
    has_pickle_tail = dvfa_name.find("pickle")
    if has_pickle_tail < 0:
        pickle_out = open("{}/{}.pickle".format(path, dvfa_name), "wb")
    else:
        pickle_out = open("{}/{}".format(path, dvfa_name), "wb")

    pickle.dump(dvfa, pickle_out)
    pickle_out.close()


# Test
if __name__ == "__main__":
    from DVFApy.state import State
    import os

    state1 = State("s1", False)
    state2 = State("s2", False)
    state3 = State("s2", True)
    sink = State("sink", False)

    state1.add_transition("x1", state2)

    state2.add_transition("x1", state3)
    state2.add_transition("y", state3)

    # create sink transitions
    state3.add_transition("y", sink)

    sink.add_transition("y", sink)
    sink.add_transition("x1", sink)

    dvfa = DVFA("x1_x1", state1)

    cwd = os.getcwd()
    print(cwd)

    save(dvfa, cwd, dvfa.name)
