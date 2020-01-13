import DVFApy as dvfa_tool


def create_word_longer_than_1() -> dvfa_tool.dvfa.DVFA:
    # Accepting all word that are longer than 1
    # Create States
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", True)

    # Create Transitions
    state1.add_transition(symbol="y", state=state2)
    state2.add_transition(symbol="y", state=state3)
    state3.add_transition(symbol="y", state=state3)


    dvfa = dvfa_tool.dvfa.DVFA(name="w>1", starting_state=state1)
    return dvfa


def create_1_2() -> dvfa_tool.dvfa.DVFA:
    # Accepting the word "1, 2"
    # Create States
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", True)

    sink = dvfa_tool.state.State("sink", True)

    # Create Transitions
    state1.add_transition(symbol=1, state=state2)
    state1.add_transition(symbol=2, state=sink)

    state2.add_transition(symbol=2, state=state3)
    state2.add_transition(symbol=1, state=sink)

    state1.add_transition(symbol="y", state=sink)
    state2.add_transition(symbol="y", state=sink)

    state3.add_transition(symbol=1, state=sink)
    state3.add_transition(symbol=2, state=sink)
    state3.add_transition(symbol="y", state=sink)

    sink.add_transition(symbol="y", state=sink)
    sink.add_transition(symbol=1, state=sink)
    sink.add_transition(symbol=2, state=sink)

    dvfa = dvfa_tool.dvfa.DVFA(name="1->2", starting_state=state1)

    return dvfa


def create_3PAL_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Accepting palindromes in length of 3

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

    dvfa = dvfa_tool.dvfa.DVFA(name="3PAL", starting_state=state1)
    return dvfa


def create_1_x_plus_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Accepting (1 x_1)^+

    # Create States
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", True)
    state4 = dvfa_tool.state.State("s4", False)
    sink1 = dvfa_tool.state.State("sink1", False)
    sink2 = dvfa_tool.state.State("sink2", False)

    # Create Transitions
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

    # Create Sink Transitions
    sink1.add_transition("y", sink1)
    sink1.add_transition(1, sink1)

    sink2.add_transition("x1", sink2)
    sink2.add_transition("y", sink2)
    sink2.add_transition(1, sink2)

    dvfa = dvfa_tool.dvfa.DVFA(name="1_X_plus", starting_state=state1)
    return dvfa


def create_herring_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Accepting 1 2 3 , afterwards x_1 and x_2 are optional

    # Create States
    state1 = dvfa_tool.state.State("s1", False)
    state2 = dvfa_tool.state.State("s2", False)
    state3 = dvfa_tool.state.State("s3", False)
    state4 = dvfa_tool.state.State("s4", True)
    state5 = dvfa_tool.state.State("s5", True)
    state6 = dvfa_tool.state.State("s6", True)
    sink1 = dvfa_tool.state.State("sink1", False)
    sink2 = dvfa_tool.state.State("sink2", False)
    sink3 = dvfa_tool.state.State("sink3", False)

    # Create Transitions
    state1.add_transition(state=state2, symbol=1)
    state2.add_transition(state=state3, symbol=2)
    state3.add_transition(state=state4, symbol=3)
    state4.add_transition(state=state5, symbol="x1")
    state5.add_transition(state=state6, symbol="x2")

    # Create Sink Transitions
    state1.add_transition(state=sink1, symbol=2)
    state1.add_transition(state=sink1, symbol=3)
    state1.add_transition(state=sink1, symbol="y")

    state2.add_transition(state=sink1, symbol=1)
    state2.add_transition(state=sink1, symbol=3)
    state2.add_transition(state=sink1, symbol="y")

    state3.add_transition(state=sink1, symbol=1)
    state3.add_transition(state=sink1, symbol=2)
    state3.add_transition(state=sink1, symbol="y")

    state4.add_transition(state=sink1, symbol=1)
    state4.add_transition(state=sink1, symbol=2)
    state4.add_transition(state=sink1, symbol=3)

    state5.add_transition(state=sink2, symbol=1)
    state5.add_transition(state=sink2, symbol=2)
    state5.add_transition(state=sink2, symbol=3)
    state5.add_transition(state=sink2, symbol="x1")

    state6.add_transition(state=sink3, symbol=1)
    state6.add_transition(state=sink3, symbol=2)
    state6.add_transition(state=sink3, symbol=3)
    state6.add_transition(state=sink3, symbol="x1")
    state6.add_transition(state=sink3, symbol="x2")
    state6.add_transition(state=sink3, symbol="y")

    sink1.add_transition(state=sink1, symbol=1)
    sink1.add_transition(state=sink1, symbol=2)
    sink1.add_transition(state=sink1, symbol=3)
    sink1.add_transition(state=sink1, symbol="y")

    sink2.add_transition(state=sink2, symbol=1)
    sink2.add_transition(state=sink2, symbol=2)
    sink2.add_transition(state=sink2, symbol=3)
    sink2.add_transition(state=sink2, symbol="x1")
    sink2.add_transition(state=sink2, symbol="y")

    sink3.add_transition(state=sink3, symbol=1)
    sink3.add_transition(state=sink3, symbol=2)
    sink3.add_transition(state=sink3, symbol=3)
    sink3.add_transition(state=sink3, symbol="x1")
    sink3.add_transition(state=sink3, symbol="x2")
    sink3.add_transition(state=sink3, symbol="y")

    dvfa = dvfa_tool.dvfa.DVFA(name="herring", starting_state=state1)
    return dvfa


def create_sink_DVFA() -> dvfa_tool.dvfa.DVFA:
    # Accepting nothing
    # Create States
    state1 = dvfa_tool.state.State("s1", False)

    # Create Transitions
    state1.add_transition(symbol="y", state=state1)

    dvfa = dvfa_tool.dvfa.DVFA(name="sink", starting_state=state1)
    return dvfa