
class TickerNotFoundError(Exception):
    """
    Exception raised when the inputted ticker is not found

    :param ticker (string): the inputted ticker to the query
    :param message (string, optional): the message to display
    """

    def __init__(self, ticker, message="the inputted ticker '{ticker}' could not be found"):
        self.ticker = ticker
        self.message = message.format(ticker=self.ticker)
        super().__init__(self.message)


class NestedDepthError(Exception):
    """
    Exception raised when the inputted nested iterable is the incorrect depth

    :param input_depth (int): the depth of the inputted iterable
    :param correct_depth (int or iterable): the correct depth(s) of the iterable
    """

    def __init__(self, input_depth, correct_depth, message="the nested depth of the iterable ({input_depth}) is invalid for required depth ({correct_depth})"):
        self.input_depth = input_depth
        self.correct_depth = correct_depth
        self.message = message.format(input_depth=self.input_depth, correct_depth=self.correct_depth)
        super().__init__(self.message)
