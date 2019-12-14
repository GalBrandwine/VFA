class Word:
    """ Simple word implementation. """

    def __init__(self, input_word: list):
        self._word = input_word

    def __str__(self):
        return "{}".format(self._word)

    @property
    def word(self) -> list:
        return self._word

    def get_word_length(self):
        return len(self._word)

    def get_letter(self, index) -> int:
        return self._word[index]


