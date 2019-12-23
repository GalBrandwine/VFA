import DVFApy as dvfa_tool


# **************************************** TESTING helpers ****************************************
def create_3PAL_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Creating palindrome in length of 3

    # setup
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", False)
    state4 = dvfa_tool.state.State("s4", True)
    sink = dvfa_tool.state.State("sink", False)

    state1.add_transition("x1", state2)

    state2.add_transition("x1", state3)
    state2.add_transition("y", state3)

    state3.add_transition("x1", state4)

    # create sink transitions
    state3.add_transition("y", sink)

    state4.add_transition("y", sink)
    state4.add_transition("x1", sink)

    sink.add_transition("y", sink)
    sink.add_transition("x1", sink)

    dvfa = dvfa_tool.dvfa.DVFA("3PAL", state1)
    return dvfa


def create_1_x_plus_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Creating palindroms in length of 3

    # setup
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", True)
    state4 = dvfa_tool.state.State("s4", False)
    sink1 = dvfa_tool.state.State("sink1", False)
    sink2 = dvfa_tool.state.State("sink2", False)

    state1.add_transition(1, state2)
    state1.add_transition("y", sink1)

    state2.add_transition("x1", state3)
    state2.add_transition(1, sink1)

    state3.add_transition("x1", sink2)
    state3.add_transition("y", sink2)
    state3.add_transition(1, state4)

    state4.add_transition("x1", state3)
    state4.add_transition("y", sink2)
    state4.add_transition(1, sink2)

    # Create sink transitions
    sink1.add_transition("y", sink1)
    sink1.add_transition(1, sink1)

    sink2.add_transition("x1", sink2)
    sink2.add_transition("y", sink2)
    sink2.add_transition(1, sink2)

    dvfa = dvfa_tool.dvfa.DVFA("1_X_plus", state1)
    return dvfa
