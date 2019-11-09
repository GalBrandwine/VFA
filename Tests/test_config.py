from DVFApy.word import Word
from DVFApy.state import State
from DVFApy.config import Config


class TestConfig:
    def test_current_state(self):
        # setup

        # create stuff for new config:
        temp_state = State("Alons_first_state", True)
        temp_word = Word([1, 123, 44])
        temp_bound_variable = dict()

        # run
        temp_config = Config(temp_state, temp_word, temp_bound_variable)

        # test
        assert temp_config.current_state == temp_state

    def test_bound_variables_map(self):
        # setup

        temp_state = State("Alons_first_state", True)
        temp_word = Word([1, 123, 44])
        temp_bound_variable = dict()

        # run

        # dict.key is current letter on a run
        # dict.value is Variable name
        temp_bound_variable[123] = "x1"
        temp_config = Config(temp_state, temp_word, temp_bound_variable)

        # test
        assert temp_config.bound_variables_map[123] == "x1"

    def test_is_current_state_accepting(self):
        # setup
        # create stuff for new config:
        temp_state = State("Alons_first_state", True)
        temp_word = Word([1, 123, 44])
        temp_bound_variable = dict()

        # run
        temp_config = Config(temp_state, temp_word, temp_bound_variable)

        # test
        assert temp_config.is_current_state_accepting() is True

    def test_has_finished(self):
        # This test suppose to FAIL!
        # We are creating a CONFIG with a word that is not empty
        # and testing if we have finished

        # setup
        # create stuff for new config:
        temp_state = State("Alons_first_state", True)
        temp_remain_word = Word([1, 123, 44])
        temp_bound_variable = dict()

        # run
        temp_config = Config(temp_state, temp_remain_word, temp_bound_variable)

        # test
        assert temp_config.has_finished() is True

    def test_remaining_word(self):
        # setup
        # create stuff for new config:
        temp_state = State("Alons_first_state", True)
        temp_remain_word = Word([1, 123, 44])
        temp_bound_variable = dict()

        # run
        temp_config = Config(temp_state, temp_remain_word, temp_bound_variable)

        # test
        assert temp_config.remaining_word == temp_remain_word
