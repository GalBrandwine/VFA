import DVFApy as dvfa_tool


# **************************************** TESTING helpers ****************************************
def create_3PAL_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Creating palindroms in length of 3

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

    dvfa = dvfa_tool.dvfa.DVFA(state1)
    return dvfa
