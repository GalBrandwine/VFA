import DVFApy as dvfa_tool
from Utils import dvfa_generator


class TestDVFA:
    def test_starting_state(self):
        self.fail()

    def test__map_properties(self):
        self.fail()

    def test_unwind(self):
        """Tset for unwinding functionality."""
        # setup
        word = dvfa_tool.word.Word([1, 2, 2])

        dvfa = dvfa_generator.create_3PAL_DVFA()

        # run
        unwinded_dvfa, unwind_dict = dvfa_tool.dvfa.DVFA.unwind(dvfa)

        # test
        assert len(unwinded_dvfa.var_set) == len(dvfa.var_set)
        assert len(unwinded_dvfa.const_set) == len(dvfa.const_set)

        # Checking language of unwinded vs standard 3PAL

        break_flag = False
        config = None
        word = dvfa_tool.word.Word([1])
        run = dvfa_tool.run.Run(unwinded_dvfa, word)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

        break_flag = False
        config = None
        word = dvfa_tool.word.Word([1, 2, 1])
        run = dvfa_tool.run.Run(unwinded_dvfa, word)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is True

        break_flag = False
        config = None
        word = dvfa_tool.word.Word([1, 3, 1, 4, 5])
        run = dvfa_tool.run.Run(unwinded_dvfa, word)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False