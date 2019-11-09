from DVFApy.word import Word
from DVFApy.state import State
from DVFApy.dvfa import DVFA
from DVFApy.run import Run


class TestRun():
    def test_next_state(self):
        # In this test we testing if performing a transition
        # creates all the propertis of a config correctly

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
