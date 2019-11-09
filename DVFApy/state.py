class State:
    def __init__(self, name=None, is_accepting=False):
        self._transition_map = dict()
        self.is_accepting = is_accepting
        self.name = name

    def add_transition(self, symbol, state):
        self._transition_map[symbol] = state

    def transition(self, letter):
        return self._transition_map[letter]

    @property
    def transition_map(self):
        return self._transition_map