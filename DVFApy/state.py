class State:
    def __init__(self, name: str = None, is_accepting: bool = False) -> object:
        """

        :rtype: object
        """
        self._transition_map = dict()
        self._is_accepting = is_accepting
        self.name = name

    def add_transition(self, symbol, state):
        self._transition_map[symbol] = state

    def transition(self, letter):
        # Returns a the next State.
        return self._transition_map[letter]

    @property
    def transition_map(self):
        return self._transition_map

    @property
    def is_accepting(self):
        return self._is_accepting

