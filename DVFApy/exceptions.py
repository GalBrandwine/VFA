class DvfaException(Exception):
    """Generic exception for DVFApy"""

    def __init__(self, msg="DVFA Error", original_exception=None):
        super(DvfaException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
