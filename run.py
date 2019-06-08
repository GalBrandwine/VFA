class Run:
    """Run is a class for maintaing a run of vfa over a given word."""

    def __init__(self, logger, vfa, word):
        self.logger = logger
        self.vfa = vfa
        self.word = word

    def run(self):
        # todo: implement run of vfa over word.
        self.logger.info("run started")
