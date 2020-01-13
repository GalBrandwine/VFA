from DVFApy.state import State
from DVFApy.word import Word


class Config:
    """
    Config is a run snapshot.

    With config, we can know run state for debugging purposes.
    """

    def __init__(self, current_state: State, remaining_word: Word, bound_variables: dict,
                 y_was_read: bool = False) -> object:
        self._current_state = current_state
        self._bound_variables = bound_variables
        self._remaining_word = remaining_word  # the letters that stil needed to be read
        self._y_was_read = y_was_read

    @property  # python getter
    def current_state(self):
        return self._current_state

    @property
    def bound_variables_map(self) -> dict:
        return self._bound_variables

    @property
    def remaining_word(self) -> Word:
        return self._remaining_word

    @property
    def is_y_read(self) -> bool:
        return self._y_was_read

    def set_y_read(self):
        self._y_was_read = True

    def is_current_state_accepting(self) -> bool:
        # stating if the state we are on is accepting
        return self._current_state.is_accepting

    def has_finished(self) -> bool:
        return True if self._remaining_word.get_word_length() is 0 else False
