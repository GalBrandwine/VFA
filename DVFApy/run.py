import time
from DVFApy.config import Config
from DVFApy.dvfa import DVFA
from DVFApy.word import Word
from DVFApy.state import State


class Run:
    """Run is a class for maintaing a run of dvfa over a given word.

    In order to perform a run, the function next_state should be called in a loop."""

    def __init__(self, dvfa: DVFA, word: Word):
        self._dvfa: DVFA = dvfa
        self._word: Word = word
        self._index: int = 0
        self._bound_variables: dict = dict()  # {key: int, value: string}

        self._current_config = Config(self._dvfa.starting_state, self._word, self._bound_variables)

    def next_state(self) -> Config:
        next_state: State = None
        # get the current letter from remaining letters in Word
        current_letter = self._word.get_letter(self._index)

        # Get our "Running history".
        # this map holds all the letters that we have seen in previews states,
        # and  their's values are the assigns variables OR a constant.
        current_bound_variable_map = self._current_config.bound_variables_map

        # try to get from the current variable_map the variable that was assigned to the current letter.
        variable_name = current_bound_variable_map.get(current_letter, None)

        if current_letter in self._dvfa.const_set:
            # Current letter is a vdfa constant.
            # So we can make a transition on the constant that
            # has the same value as current_letter.
            next_state = self._current_config.current_state.transition(current_letter)
        elif variable_name is None:
            # letter is currently not assigned to variable, this means that we havnt seen this letter yet,
            # OR it is a DVFA constant.
            pass
        elif current_letter in self._dvfa.var_set:
            # letter is assign to variable.
            # NOTE: if variable_name is not None  AND there's no transition, than the DVFA is not legal.
            next_state = self._current_config.current_state.transition(variable_name)
        else:
            raise Exception(
                "NOT LEGAL SITUATION: theres an unassigned letter, with ")  # TODO: implement library logic exceptions

        self._index = self._index + 1
        remaining_word = Word(self._word.word[self._index:])
        self._current_config = Config(next_state, remaining_word, current_bound_variable_map)

        return self._current_config

    # def run(self):
    #     # todo: implement run of dvfa over word.
    #     self.is_running = True
    #     print("run started")
    #
    #     # *************************************** STUPID LOOP FOR SHOWING DEBUG WORKS!!! *******************************
    #     for i in range(0, 30):
    #         if self.stop_flag is False:
    #             self.logger.info(i)
    #             time.sleep(0.5)
    #         else:
    #             break
    #
    #     self.is_running = False

    # def stop(self):
    #     self.stop_flag = True
    #     print("run stopped")
