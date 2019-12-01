from DVFApy.state import State


class DVFA:
    """Class for holding a DVFA. """

    def __init__(self, starting_state: State = None):
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
        u_states_dict = dict();
        u_state = DVFA._recursive_unwinding(A, current_tuple=None, tuple_set=None, u_states_dict=u_states_dict, is_first=True)
        return DVFA(u_state), u_states_dict

    @staticmethod
    def _recursive_unwinding(A, current_tuple: tuple, tuple_set: set, u_states_dict:dict, is_first: bool) -> State:
        """

        :param A: a DVFA
        :param current_tuple: a tuple of a state and a list of all tha variables read to reach this state
        :param tuple_set: the set of all the tuples.
        :return: U_start_state.
        """
        if is_first:
            starting_tuple = (A.starting_state, frozenset())
            tuple_set = set()
            tuple_set.add(starting_tuple)
            current_tuple = starting_tuple

        # construct the name of the result state.
        new_name = "{0} {{1}}".format(current_tuple[0].name, ",".join(current_tuple[1]))
        is_accepting = current_tuple[0].is_accepting
        new_state = State(name=new_name, is_accepting=is_accepting)
        u_states_dict.update({current_tuple: new_state})

        result_map = dict()
        for symbol, next_state in current_tuple[0].transition_map.items():
            # iterate on all {symbol,state} transition of this state.
            next_symbols = set()
            if symbol == "y":
                # optimization.
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


            if (next_state, next_symbols) in u_states_dict.keys():
                result_state = u_states_dict[(next_state, next_symbols)]
            else:
                next_tuple = (next_state, next_symbols)
                tuple_set.add(next_tuple)

                result_state = DVFA._recursive_unwinding(A=A,
                                                         current_tuple=next_tuple,
                                                         tuple_set=tuple_set,
                                                         u_states_dict=u_states_dict,
                                                     is_first=False)
                result_map[symbol] = result_state

        for sym, state in result_map.items():
            new_state.add_transition(sym, state)
        return new_state
