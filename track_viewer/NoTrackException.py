

class NoTrackException(Exception):
    """ Exceptio raised when trying to work with a null track """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message