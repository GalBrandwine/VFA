import DVFApy as dvfa_tool
from Utils import dvfa_generator


class TestDVFA:
    def test_unwind_3PAL(self):
        """Test for unwinding functionality."""
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

    def test_unwind_1_x_plus(self):
        """Test for unwinding functionality."""
        # setup
        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1, 2])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        dvfa = dvfa_generator.create_1_x_plus_DVFA()

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
        assert config.is_current_state_accepting() is False

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word4)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is True

        break_flag = False
        run = dvfa_tool.run.Run(unwinded_dvfa, word5)
        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

    def test_map_properties(self):
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        assert len(dvfa_3pal.const_set) is 0
        assert len(dvfa_3pal.var_set) is 1

        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        assert len(dvfa_1_x_plus.const_set) is 1
        assert len(dvfa_1_x_plus.var_set) is 1

    def test_copy_3pal(self):
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_3pal_copy = dvfa_3pal.copy()

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            expected_run = dvfa_tool.run.Run(dvfa=dvfa_3pal, word=word).run()
            actual_run = dvfa_tool.run.Run(dvfa=dvfa_3pal_copy, word=word).run()
            assert expected_run == actual_run

    def test_copy_1_x_plus(self):
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_1_x_plus_copy = dvfa_1_x_plus.copy()

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1, 2])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            expected_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus, word=word).run()
            actual_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus_copy, word=word).run()
            assert expected_run == actual_run

    def test_complement_3pal(self):
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_3pal_complement = dvfa_3pal.complement()

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            expected_run = dvfa_tool.run.Run(dvfa=dvfa_3pal, word=word).run()
            actual_run = dvfa_tool.run.Run(dvfa=dvfa_3pal_complement, word=word).run()
            assert expected_run != actual_run

    def test_complement_1_x_plus(self):
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_1_x_plus_complement = dvfa_1_x_plus.complement()

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1, 2])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            expected_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus, word=word).run()
            actual_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus_complement, word=word).run()
            assert expected_run != actual_run
