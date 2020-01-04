class DvfaException(Exception):
    """Generic exception for DVFApy"""

    def __init__(self, msg, original_exception):
        super(DvfaException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
