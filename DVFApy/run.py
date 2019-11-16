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

            # Now we want to perform the transition.
            next_state = self._current_config.current_state.transition(current_letter)

        elif variable_name is None:
            # Letter is currently not assigned to variable, this means that we havn't seen this letter yet,

            """ Get U (group) of all [U,V] of these state
             1. get symbols set of current state (in gals simple and ignorance language - the U of the [U,V] )
             2. subscribe from U the dvfa constat group.
             3. subscribe from U the assigned variables.
             
             4. the result of all this action suppose to be group with 1 elemnt ONLY! If else it is not a deterministic DVFA.
             """
            current_state_symbol_set = set(self._current_config.current_state.transition_map.keys())
            current_state_symbol_set = current_state_symbol_set - self._dvfa.const_set
            current_state_symbol_set = current_state_symbol_set - set(self._current_config.bound_variables_map.values())
            if len(current_state_symbol_set) is not 1:
                raise Exception(
                    "NOT LEGAL SITUATION: more than one edge from this state onward (not deterministic) ")  # TODO: implement library logic exceptions
            else:
                # Transition is legal, current_state_symbol_set containing only one element,
                # which this element is the unbounded variable.
                # Now we are assigning the variable to the current letter,
                # and adding the couple to current state bound variable map.

                symbol = current_state_symbol_set.pop()

                if symbol == 'y':
                    # If symbol is "y", that mean it is a WILDCARD,
                    # we can pass on any letter that that hasnt beet assigned to variable, and it is not a constant.

                    # only action: set current config.y_has_read flag to true.
                    self._current_config.set_y_read()

                elif self._current_config.is_y_read is True:
                    # If symbol is not "Y" AND we have transitioned on "Y" before,
                    # and we seeing an un assigned new variable,
                    # this is not a legal situation.
                    raise Exception(
                        "NOT LEGAL SITUATION: current variable is NOT Y, but Y has been read. (not deterministic) ")  # TODO: implement library logic exception
                else:
                    # symbol is not "y", and we haven't seen "y" before.
                    self._current_config.bound_variables_map[current_letter] = symbol

                # Now we want to perform the transition.
                next_state = self._current_config.current_state.transition(symbol)

        elif variable_name in self._dvfa.var_set:
            # letter is assign to variable.
            # NOTE: if variable_name is not None  AND there's no transition, than the DVFA is not legal.
            next_state = self._current_config.current_state.transition(variable_name)
        else:
            raise Exception(
                "NOT LEGAL SITUATION: theres an unassigned letter, with ")  # TODO: implement library logic exceptions

        self._index = self._index + 1
        remaining_word = Word(self._word.word[self._index:])
        self._current_config = Config(next_state, remaining_word, current_bound_variable_map,
                                      self._current_config.is_y_read)

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
