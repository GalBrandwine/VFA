import itertools
import sys

import DVFApy as dvfa_tool
from Utils import dvfa_generator
from Utils import word_generator


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
        assert len(unwinded_dvfa.var_set) == len(dvfa._var_set)
        assert len(unwinded_dvfa.const_set) == len(dvfa._const_set)

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
        assert len(unwinded_dvfa.var_set) == len(dvfa._var_set)
        assert len(unwinded_dvfa.const_set) == len(dvfa._const_set)

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
        assert len(dvfa_3pal._const_set) is 0
        assert len(dvfa_3pal._var_set) is 1

        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        assert len(dvfa_1_x_plus._const_set) is 1
        assert len(dvfa_1_x_plus._var_set) is 1

    def test_copy_3pal(self):
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_3pal_copy = dvfa_tool.dvfa.DVFA.copy(dvfa_3pal)

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
        dvfa_1_x_plus_copy = dvfa_tool.dvfa.DVFA.copy(dvfa_1_x_plus)

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
        dvfa_3pal_complement = dvfa_tool.dvfa.DVFA.complement(dvfa_3pal)

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            original_run = dvfa_tool.run.Run(dvfa=dvfa_3pal, word=word).run()
            complementing_run = dvfa_tool.run.Run(dvfa=dvfa_3pal_complement, word=word).run()
            assert original_run != complementing_run

    def test_complement_1_x_plus(self):
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_1_x_plus_complement = dvfa_tool.dvfa.DVFA.complement(dvfa_1_x_plus)

        word1 = dvfa_tool.word.Word([1, 2, 2])
        word2 = dvfa_tool.word.Word([1, 2, 1, 2])
        word3 = dvfa_tool.word.Word([1, 1, 1])
        word4 = dvfa_tool.word.Word([1, 2])
        word5 = dvfa_tool.word.Word([1, 2, 3, 2, 2, 1])

        word_list = [word1, word2, word3, word4, word5]

        for word in word_list:
            original_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus, word=word).run()
            complementing_run = dvfa_tool.run.Run(dvfa=dvfa_1_x_plus_complement, word=word).run()
            assert original_run != complementing_run

    def test_intersect(self):
        # Setup
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_herring = dvfa_generator.create_herring_DVFA()
        dvfa_longer_than_1 = dvfa_generator.create_word_longer_than_1()
        dvfa_1_2 = dvfa_generator.create_1_2()

        dvfa_list = [dvfa_3pal, dvfa_1_2, dvfa_herring, dvfa_longer_than_1, dvfa_1_x_plus]
        word_list = word_generator.get_words()

        for dvfa1, dvfa2 in itertools.product(dvfa_list, dvfa_list):

            # Run
            try:
                intersect_dvfa = dvfa_tool.dvfa.DVFA.intersect(dvfa1, dvfa2)
            except KeyError:
                print("intersection of automata {} and {} failed!".format(dvfa1.name, dvfa2.name))
                assert False
            for word in word_list:
                a1_run = dvfa_tool.run.Run(dvfa=dvfa1, word=word).run()
                a2_run = dvfa_tool.run.Run(dvfa=dvfa2, word=word).run()
                try:
                    intersect_run = dvfa_tool.run.Run(dvfa=intersect_dvfa, word=word).run()
                    # Test
                    assert intersect_run == (
                            a1_run and a2_run), "result of run on word {} on intersect automata {} failed!".format(
                        word.word, intersect_dvfa.name)
                except KeyError:
                    print(
                        "run of run on word {} on intersect automata {} failed!".format(word.word, intersect_dvfa.name))
                    assert False

    def test_union(self):
        # Setup
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_herring = dvfa_generator.create_herring_DVFA()
        dvfa_longer_than_1 = dvfa_generator.create_word_longer_than_1()
        dvfa_1_2 = dvfa_generator.create_1_2()

        dvfa_list = [dvfa_3pal, dvfa_1_2, dvfa_herring, dvfa_longer_than_1, dvfa_1_x_plus]
        word_list = word_generator.get_words()

        for dvfa1, dvfa2 in itertools.product(dvfa_list, dvfa_list):

            # Run
            try:
                union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa1, dvfa2)
            except KeyError:
                print("union of automata {} and {} failed!".format(dvfa1.name, dvfa2.name))
                assert False
            for word in word_list:
                a1_run = dvfa_tool.run.Run(dvfa=dvfa1, word=word).run()
                a2_run = dvfa_tool.run.Run(dvfa=dvfa2, word=word).run()
                try:
                    intersect_run = dvfa_tool.run.Run(dvfa=union_dvfa, word=word).run()
                    # Test
                    assert intersect_run == (
                            a1_run or a2_run), "result of run on word {} on union automata {} failed!".format(
                        word.word, union_dvfa.name)
                except KeyError:
                    print("run of run on word {} on intersect automata {} failed!".format(word.word, union_dvfa.name))
                    assert False

    def test_big_union(self):
        # Setup
        dvfa_1_x_plus = dvfa_generator.create_1_x_plus_DVFA()
        dvfa_3pal = dvfa_generator.create_3PAL_DVFA()
        dvfa_herring = dvfa_generator.create_herring_DVFA()
        dvfa_longer_than_1 = dvfa_generator.create_word_longer_than_1()
        dvfa_1_2 = dvfa_generator.create_1_2()

        dvfa_list = [dvfa_3pal, dvfa_1_2, dvfa_herring, dvfa_longer_than_1]
        word_list = word_generator.get_words()

        union_dvfa: dvfa_tool.DVFA = dvfa_1_x_plus
        for dvfa in dvfa_list:

            # Run
            try:
                union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa, union_dvfa)
            except KeyError:
                print("union of automata {} and {} failed!".format(dvfa.name, union_dvfa.name))
                assert False
            for word in word_list:
                a1_run = dvfa_tool.run.Run(dvfa=dvfa, word=word).run()
                a2_run = dvfa_tool.run.Run(dvfa=union_dvfa, word=word).run()
                try:
                    intersect_run = dvfa_tool.run.Run(dvfa=union_dvfa, word=word).run()
                    # Test
                    assert intersect_run == (
                            a1_run or a2_run), "result of run on word {} on union automata {} failed!".format(
                        word.word, union_dvfa.name)
                except KeyError:
                    print("run of run on word {} on intersect automata {} failed!".format(word.word, union_dvfa.name))
                    assert False

    def test_emptiness_false(self):
        # Setup
        dvfa = dvfa_generator.create_herring_DVFA()

        # Run
        is_empty = dvfa_tool.dvfa.DVFA.emptiness(dvfa)

        # Test
        assert not is_empty

    def test_emptiness_true(self):
        # Setup
        dvfa = dvfa_generator.create_sink_DVFA()

        # Run
        is_empty = dvfa_tool.dvfa.DVFA.emptiness(dvfa)

        # Test
        assert is_empty

    def test_emptiness_with_intersect(self):
        # Setup
        dvfa1 = dvfa_generator.create_3PAL_DVFA()
        dvfa2 = dvfa_tool.dvfa.DVFA.complement(dvfa1)
        empty_dvfa = dvfa_tool.dvfa.DVFA.intersect(dvfa1, dvfa2)

        # Run
        is_empty = dvfa_tool.dvfa.DVFA.emptiness(empty_dvfa)

        # Test
        assert is_empty

    def test_emptiness_with_union(self):
        # Setup
        dvfa1 = dvfa_generator.create_3PAL_DVFA()
        dvfa2 = dvfa_tool.dvfa.DVFA.complement(dvfa1)
        union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa1, dvfa2)

        # Run
        is_empty = dvfa_tool.dvfa.DVFA.emptiness(union_dvfa)

        # Test
        assert not is_empty

    def test_determinism(self):
        # Setup
        dvfa1 = dvfa_generator.create_3PAL_DVFA()

        # Run
        is_det = dvfa_tool.dvfa.DVFA.determinism(dvfa1)

        # Test
        assert is_det

    def test_not_determinism_test_1(self):
        """
            I) For each state, every constant exits that state.
            II) Each state either introduce one new bound variable or free variable "y", but not both.
            III) Once a free variable is read, no new bound variables are created, this can be known by unwinding.
        """
        # Setup
        state_1 = dvfa_tool.state.State(name="s1", is_accepting=False)
        state_2 = dvfa_tool.state.State(name="s2", is_accepting=False)
        state_3 = dvfa_tool.state.State(name="s3", is_accepting=True)

        # First test constrain.
        state_1.add_transition("x1", state_2)
        state_1.add_transition(1, state_3)

        dvfa1 = dvfa_tool.dvfa.DVFA(starting_state=state_1)

        # Run
        is_det = dvfa_tool.dvfa.DVFA.determinism(dvfa1)

        # Test
        assert is_det is False

    def test_not_determinism_test_2(self):
        """
            II) Each state either introduce one new bound variable or free variable "y", but not both.
        """
        # Setup
        state_1 = dvfa_tool.state.State(name="s1", is_accepting=False)
        state_2 = dvfa_tool.state.State(name="s2", is_accepting=False)

        # Seccond test constrain.
        state_1.add_transition("x1", state_2)
        state_1.add_transition("y", state_2)

        dvfa1 = dvfa_tool.dvfa.DVFA(starting_state=state_1)

        # Run
        is_det = dvfa_tool.dvfa.DVFA.determinism(dvfa1)

        # Test
        assert is_det is False

    def test_not_determinism_test_3(self):
        """
            III) Once a free variable is read, no new bound variables are created, this can be known by unwinding.
        """
        # Setup
        state_1 = dvfa_tool.state.State(name="s1", is_accepting=False)
        state_2 = dvfa_tool.state.State(name="s2", is_accepting=False)
        state_3 = dvfa_tool.state.State(name="s3", is_accepting=False)
        # Third test constrain.

        state_1.add_transition("y", state_2)
        state_2.add_transition("x1", state_2)

        dvfa1 = dvfa_tool.dvfa.DVFA(starting_state=state_1)

        # Run
        is_det = dvfa_tool.dvfa.DVFA.determinism(dvfa1)

        # Test
        assert is_det is False

    def test_scaleable(self):
        dvfa1 = dvfa_generator.create_symmetrical_i_n_minus_i(n = 3, i = 2)
        dvfa2 = dvfa_generator.create_symmetrical_i_n_minus_i(n = 5, i = 3)

        word1 = dvfa_tool.word.Word([1, 2, 1])
        word2 = dvfa_tool.word.Word([3, 5, 7, 2, 2, 3])

        res1 = dvfa_tool.run.Run(dvfa=dvfa1,word=word1).run()
        res2 = dvfa_tool.run.Run(dvfa=dvfa2,word=word2).run()

        assert res1
        assert res2
        assert dvfa_tool.dvfa.DVFA.determinism(dvfa1)
        assert dvfa_tool.dvfa.DVFA.determinism(dvfa2)

    def test_scaleable_union(self):
        dvfa1 = dvfa_generator.create_symmetrical_i_n_minus_i(n=3, i=2)
        dvfa2 = dvfa_generator.create_symmetrical_i_n_minus_i(n=5, i=3)

        union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa1,dvfa2)

        word1 = dvfa_tool.word.Word([1, 2, 1])
        word2 = dvfa_tool.word.Word([3, 5, 7, 2, 2])
        word3 = dvfa_tool.word.Word([3, 3, 7, 1, 1])

        res1 = dvfa_tool.run.Run(dvfa=union_dvfa, word=word1).run()
        res2 = dvfa_tool.run.Run(dvfa=union_dvfa, word=word2).run()
        res3 = dvfa_tool.run.Run(dvfa=union_dvfa, word=word3).run()

        assert res1
        assert res2
        assert not res3

    def test_recursion_limit_union(self):
        dvfa1 = dvfa_generator.create_symmetrical_i_n_minus_i(n=3000, i=500)
        dvfa2 = dvfa_generator.create_symmetrical_i_n_minus_i(n=5555, i=300)
        current_recursion_limit = sys.getrecursionlimit()
        try:
            union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa1, dvfa2, max_recursion_depth=10)
            assert False
        except RecursionError as e:
            assert current_recursion_limit == sys.getrecursionlimit()

    def test_big_scaleable_union(self):
        dvfa1 = dvfa_generator.create_symmetrical_i_n_minus_i(n=500, i=50)
        dvfa2 = dvfa_generator.create_symmetrical_i_n_minus_i(n=750, i=75)

        union_dvfa = dvfa_tool.dvfa.DVFA.union(dvfa1, dvfa2)
