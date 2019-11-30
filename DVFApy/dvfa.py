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
        starting_tuple = [A.starting_state, {}]

        tuple_set = set()
        tuple_set.add(starting_tuple)
        u_state = DVFA._recursive_unwinding(A, starting_tuple, tuple_set)
        return DVFA(u_state), tuple_set

    @staticmethod
    def _recursive_unwinding(A, current_tuple: tuple, tuple_set: set) -> State:
        """

        :param A: a DVFA
        :param current_tuple: a tuple of a state and a list of all tha variables read to reach this state
        :param tuple_set: the set of all the tuples.
        :return: U_start_state.
        """
        result_map = map()
        for symbol, next_state in current_tuple[0].transition_map:
            # iterate on all {symbol,state} transition of this state.
            next_tuple = map()
            if symbol == "y":
                # optimization.
                # if symbol is wildcard, don't pass on all the var_set.
                next_tuple[next_state] = current_tuple[1].union(symbol)
            elif symbol in A.var_set:
                # if symbol is known as a variable or a WILDCARD in this DVFA,
                # then add it to current tuple read variables set,
                # because its a variable that was read in order to get to this state.
                next_tuple[next_state] = current_tuple[1].union(symbol)
            else:
                # if the symbol is not in this DVFA variable set.
                next_tuple[next_state] = current_tuple[1]

            if next_state in tuple_set:  # TODO: alon need to implement this
                pass
            else:
                tuple_set = tuple_set.union({next_tuple})
                result = DVFA._recursive_unwinding(A, next_tuple, tuple_set)
                result_map[symbol] = result

            # TODO: fix naming problem

            # construct the name of the result state.
            # result_state_name = result_state_name.join(current_tuple[1])

            result_state = State(current_tuple[0].name, current_tuple[0].is_accepting)
        for symbol, state in result_map:
            result_state.add_transition(symbol, state)
        return result_state
