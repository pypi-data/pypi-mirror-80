class SonolabError(Exception):
    """
    General Sonolab error
    """

    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class SL10OverError(SonolabError):
    """
    Error for when the SL10 tried to be set to a power level it couldn't be set to
    """

    def __init__(self, value):
        self.msg = f'SL10 over error, you cannot set the power to {value}'

