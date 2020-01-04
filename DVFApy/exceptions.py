class DvfaExceptions(Exception):
    """Generic exception for DVFApy"""

    def __init__(self, msg, original_exception):
        super(DvfaExceptions, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception

#
# # class DvfaNoneDeterminisem
# # runtime exceptions
# class DvfaRunFailure(DvfaExceptions):
#
# # logic expections
