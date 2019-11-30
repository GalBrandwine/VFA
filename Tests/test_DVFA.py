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
        unwinded_dvfa = dvfa_tool.dvfa.DVFA.unwind(dvfa)

        # test
        assert 1 == 1
