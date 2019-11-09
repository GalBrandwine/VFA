class DVFA:
    """Class for holding a VFA. """

    def __init__(self, starting_state=None):
        self._starting_state = starting_state
        self.var_set = {}
        self.const_set = {}
        self._map_properties()

    def _map_properties(self):
        my_bfs = {}
        visited_states = {}
        for symbol, state in self._starting_state.transition_map:

            if isinstance(symbol, str):
                if symbol != "y":
                    self.var_set.append(symbol)
            if state not in visited_states:
                visited_states.add(state)
                my_bfs.add(state)