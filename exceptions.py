class Inv(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class HeaderExtractionError(ExtractionError):
    """Exception raised for errors while extracting Headers.

    Attributes:
        expression -- expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.header = expression
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        logger.error(f'{self.header} ==> {self.message}')
        pass
