from GUI import vfa_gui


class TestVFA_gui():

    def test_raise_expection(self):
        """ test if excaption are handled in a new gui window.

        Usage: Try to open a file that is not CSV.
        """
        # setup
        vfa = vfa_gui.VFA_gui("Automata generation & verification tool", 1200, 600)

        # run
        try:
            vfa.start()
        except Exception as err:
            assert err is FileNotFoundError

    def test_run(self):
        self.fail()

    def test_unwind(self):
        self.fail()

    def test_negate(self):
        self.fail()

    def test_complete(self):
        self.fail()

    def test_intersect(self):
        self.fail()

    def test_get_inserted_word(self):
        self.fail()

    def test_generate_automata(self):
        self.fail()

    def test_open_vfa(self):
        self.fail()

    def test_create_menu(self):
        self.fail()

    def test_create_buttons(self):
        self.fail()

    def test_create_right_buttons(self):
        self.fail()

    def test_create_center_widgets(self):
        self.fail()

    def test_fill_table(self):
        self.fail()


