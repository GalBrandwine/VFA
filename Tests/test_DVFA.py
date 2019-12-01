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
        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        dvfa = dvfa_generator.create_3PAL_DVFA()

        # run
        unwinded_dvfa, unwind_dict = dvfa_tool.dvfa.DVFA.unwind(dvfa)

        # test
        assert len(unwinded_dvfa.var_set) == len(dvfa.var_set)
        assert len(unwinded_dvfa.const_set) == len(dvfa.const_set)

        # Checking language of unwinded vs standard 3PAL against 5 words
        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word1)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word2)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is True

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word3)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is True

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word4)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word5)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False