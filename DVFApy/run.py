import time


class Run:
    """Run is a class for maintaing a run of vfa over a given word."""

    def __init__(self, logger, vfa, word):
        self.logger = logger
        self.vfa = vfa
        self.word = word
        self.stop_flag = False
        self.running = False

    def __del__(self):
        print("Run closed, Adios")

    def run(self):
        # todo: implement run of vfa over word.
        self.running = True
        self.logger.info("run started")

        # *************************************** STUPID LOOP FOR SHOWING DEBUG WORKS!!! *******************************
        for i in range(0, 30):
            if self.stop_flag is False:
                self.logger.info(i)
                time.sleep(0.5)
            else:
                break

        self.running = False

    def stop(self):
        self.stop_flag = True
        self.logger.info("run stopped")
