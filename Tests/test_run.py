from DVFApy.word import Word
from DVFApy.state import State
from DVFApy.dvfa import DVFA
from DVFApy.run import Run


class TestRun:
    def test_next_state_on_constant(self):
        # In this test we testing if performing a transition
        # creates all the properties of a config correctly.
        # This test covers transition with:
        # one constant.

        # setup
        word = Word([1])

        state1 = State("s1", False)
        state2 = State("s2", True)
        state1.add_transition(1, state2)

        dvfa = DVFA(state1)

        # run
        run = Run(dvfa, word)
        config = run.next_state()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.current_state == state2
        assert config.has_finished() is True
        assert config.is_current_state_accepting() is True

    def test_next_state_on_variable(self):
        # In this test we testing if performing a transition
        # creates all the properties of a config correctly.
        # This test covers transition with:
        # one variable.

        # setup
        word = Word([1])

        state1 = State("s1", False)
        state2 = State("s2", True)
        state1.add_transition("x1", state2)

        dvfa = DVFA(state1)

        # run
        run = Run(dvfa, word)
        config = run.next_state()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.current_state == state2
        assert config.has_finished() is True
        assert config.is_current_state_accepting() is True

    def test_next_state_on_Y(self):
        # In this test we testing if performing a transition
        # creates all the properties of a config correctly.
        # This test covers transition with:
        # Y (wildcard).

        # setup
        word = Word([1])

        state1 = State("s1", False)
        state2 = State("s2", True)
        state1.add_transition("y", state2)

        dvfa = DVFA(state1)

        # run
        run = Run(dvfa, word)
        config = run.next_state()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_y_read is True
        assert config.current_state == state2
        assert config.has_finished() is True
        assert config.is_current_state_accepting() is True

    # **************************************** BRUT TESTING ****************************************
    def test_3PAL_dvfa(self):
        # test if we can properly create and run on a dvfa that accepts ALL 3pal.

        # setup
        word = Word([1, 1, 1])

        dvfa = self.create_3PAL_DVFA()

        # run
        run = Run(dvfa, word)

        break_flag = False
        config = None

        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is True

    def test_3PAL_dvfa_using_wildcard(self):
        # test if we can properly create and run on a dvfa that accepts ALL 3pal.

        # setup
        word = Word([1, 2, 1])  # this is special case - it make our DVFA use the "y" wildcard.

        dvfa = self.create_3PAL_DVFA()

        # run
        run = Run(dvfa, word)

        break_flag = False
        config = None

        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_y_read is True
        assert config.is_current_state_accepting() is True

    def test_3PAL_dvfa_accepts_only_3PAL(self):
        # test if we can properly create and run on a dvfa that accepts ALL 3pal.

        # setup
        word = Word([1, 2, 2])

        dvfa = self.create_3PAL_DVFA()

        # run
        run = Run(dvfa, word)

        break_flag = False
        config = None

        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

    def test_3PAL_dvfa_sink_works_for_reading_y_more_than_once(self):
        # test if run can run on longer words that the designated language without crushing.

        # setup
        word = Word([1, 2, 1, 3, 4, 5])

        dvfa = self.create_3PAL_DVFA()

        # run
        run = Run(dvfa, word)

        break_flag = False
        config = None

        while not break_flag:
            config = run.next_state()
            break_flag = config.has_finished()

        # test
        assert config.remaining_word.get_word_length() is 0
        assert config.is_current_state_accepting() is False

    # **************************************** TESTING helpers ****************************************
    def create_3PAL_DVFA(self) -> DVFA:
        # Creating palindroms in length of 3

        # setup
        state1 = State("s1", False)
        state2 = State("s2", False)
        state3 = State("s3", False)
        state4 = State("s4", True)
        sink = State("sink", False)

        state1.add_transition("x1", state2)
        state2.add_transition("x1", state3)
        state2.add_transition("y", state3)

        state3.add_transition("x1", state4)

        # create sink transitions
        state3.add_transition("y", sink)
        state4.add_transition("y", sink)
        state4.add_transition("x1", sink)

        sink.add_transition("y", sink)
        sink.add_transition("x1", sink)

        dvfa = DVFA(state1)
        return dvfa
