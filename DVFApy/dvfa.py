from DVFApy.state import State


class DVFA:
    """Class for holding a VFA. """

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
