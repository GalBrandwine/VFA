from DVFApy.state import State


class DVFA:
    """Class for holding a DVFA. """

    def __init__(self, name: str = None, starting_state: State = None):
        self.name = name
        self._starting_state: State = starting_state
        self.var_set: set = set()
        self.const_set: set = set()
        self._map_properties()

    @property
    def starting_state(self) -> State:
        return self._starting_state

    def _map_properties(self):
        # Our implementation of BFS,
        # in order to fill DVFA's variables set, and constants set.

        my_bfs = list()
        visited_states = set()

        my_bfs.append(self._starting_state)

        for state in my_bfs:
            for symbol, neighbor in state.transition_map.items():

                if isinstance(symbol, str):
                    if symbol != "y":
                        self.var_set.add(symbol)
                else:
                    self.const_set.add(symbol)
                if neighbor not in visited_states:
                    visited_states.add(neighbor)
                    my_bfs.append(neighbor)

    @staticmethod
    def unwind(A):
        """
        This function
        :param A: a DVFA
        :return: (unwinded_DVFA, map[key=state,value=[symbols]])
        """
        # Starting point, get first state, as
        u_states_dict = dict()
        u_state = DVFA._recursive_unwinding(A, current_tuple=None, u_states_dict=u_states_dict, is_first=True)
        return DVFA(u_state), u_states_dict

    @staticmethod
    def _recursive_unwinding(A, current_tuple: tuple, u_states_dict: dict, is_first: bool) -> State:
        """
        The first run of recursive unwinding will init current_tuple and tuple_set, this was done so that each call to
        _recursive_unwinding will create one state exactly
        :param A: The target DVFA
        :param current_tuple: The current tuple of <state, set> where set is a frozenset of the letters used to reach
        state
        :param u_states_dict: A dict containing all {tuple:state} state is from the new (unwinded) DVFA
        :param is_first: Set True for the first call, False for the rest, used to init params
        :return: State that is the first state of the DVFA
        """
        if is_first:
            # init some data structures, frozenset can be used as a key in dict, as its immutable
            starting_tuple = (A.starting_state, frozenset())
            current_tuple = starting_tuple

        # construct the result state
        # name for ex. "s1 (x1,y)"
        new_name = "{0} ({1})".format(current_tuple[0].name, ",".join(current_tuple[1]))
        # so that L(A) will be the same as L(U(A))
        is_accepting = current_tuple[0].is_accepting
        # create the state and put it in the dict, the dict has two purposes:
        # I) so that we can save newly generated states, this is done to prevent state duplication (and in some cases,
        # infinite loops)
        # II) return value to the user
        new_state = State(name=new_name, is_accepting=is_accepting)
        u_states_dict.update({current_tuple: new_state})

        # the newly minted state transition map
        transition_map = dict()

        # iterate on each {symbol,state} transition of this state.
        for symbol, next_state in current_tuple[0].transition_map.items():
            next_symbols = set()
            if symbol == "y":
                # optimization
                # if symbol is wildcard, don't pass on all the var_set.
                next_symbols = next_symbols.union(current_tuple[1])
                next_symbols.add("y")
                next_symbols = frozenset(next_symbols)
            elif symbol in A.var_set:
                # if symbol is known as a variable or a WILDCARD in this DVFA,
                # then add it to current tuple read variables set,
                # because its a variable that was read in order to get to this state.
                next_symbols = next_symbols.union(current_tuple[1])
                next_symbols.add(symbol)
                next_symbols = frozenset(next_symbols)
            else:
                # if the symbol is not in this DVFA variable set.
                next_symbols = frozenset(current_tuple[1])
            # if true - it means that the state we need already exists in u_states_dict, we can simply take an existing
            # state from the unwinded DVFA
            next_tuple = (next_state, next_symbols)
            if next_tuple in u_states_dict.keys():
                result_state = u_states_dict[(next_state, next_symbols)]
                transition_map[symbol] = result_state

            # else - we need to calculate the rest of the transitions
            else:
                result_state = DVFA._recursive_unwinding(A=A,
                                                         current_tuple=next_tuple,
                                                         u_states_dict=u_states_dict,
                                                         is_first=False)
                transition_map[symbol] = result_state

        # create the state's transition map
        for sym, state in transition_map.items():
            new_state.add_transition(sym, state)
        return new_state

    @staticmethod
    def intersect(A, B):
        """

        :param A: DVFA
        :param B: DVFA
        :return: intersected DVFA
        """
        U1, _ = DVFA.unwind(A)
        U2, _ = DVFA.unwind(B)

        u1_current_state_name = U1.starting_state.name
        u2_current_state_name = U2.starting_state.name
        is_current_state_accepting = U1.starting_state.is_accepting and U2.starting_state.is_accepting

        new_starting_state = State(name="{}_{}".format(u1_current_state_name, u2_current_state_name),
                                   is_accepting=is_current_state_accepting)

        rules_set = dict()
        rules_set[(U1.starting_state, U2.starting_state, frozenset())] = new_starting_state

        DVFA._recursive_intersect(new_starting_state, rules_set)
        return DVFA(starting_state=new_starting_state)

    @staticmethod
    def _recursive_intersect(current_state: State, rules_set: dict):
        """

        :param current_state: a State
        :param rules_set: {State1,State2,frozenset(symbol1,symbol2) }
        :return:
        """
        current_state_rules = rules_set[(_, _, current_state,)]
