
# --------------------------------------------------------------------

class ResultException(BaseException):
    pass

# --------------------------------------------------------------------

class ResultAggregate:
    """
    the aggregate results
    acts like a Singleton (init will only work once)
    """
    aggregate = {}
    def __init__(self, results: list):
        if len(ResultAggregate.aggregate) == 0:
            ResultAggregate.aggregate = { r: 0 for r in results}
            print(f"result aggregate initialized: {ResultAggregate.aggregate}")
        else:
            print("ResultAggregate can not be built more than once")

    def __repr__(self):
        return f"{self.__class__.__name__}: ({ResultAggregate.aggregate})"

    def increment(self, result: str, amount: int=1)->int:
        # increments the result by the amount (default=1)
        # returns the new total of the result
        try:
            ResultAggregate.aggregate[ result ] = ResultAggregate.aggregate[ result ] + amount
            return ResultAggregate.aggregate[ result ]
        except KeyError as ke:
            raise ResultException(f"aggregate can't increment: unrecognized result type: {result}")


    def set(self, result: str, amount: int=0) -> int:
        # resets the particular result to an amount (default: 0)
        # returns the new total of the result
        try:
            ResultAggregate.aggregate[result] = amount
            return ResultAggregate.aggregate[result]
        except KeyError as ke:
            raise ResultException(f"aggregate can't set: unrecognized result type: {result}")


# --------------------------------------------------------------------

class Result:
    """
	what happened after the event, e.g., TeamA has win/loss/tie/....
	"""

    def __init__(self, e):
        self.this_event = e     # the 'parent' event, for which this is the result
        self.next_event = None  # the 'next' event: get this from EventFactory.


class SimulatedResult(Result):
    """
	what happened after the event, e.g., TeamA has win/loss/tie/....
	there is one specific result generated as part of a simulation
	"""

    def __init__(self, e, name: str, score: tuple=None, p: float=None):
        self.this_event = e     # the 'parent' event, for which this is the result
        self.next_event = None  # the 'next' event: get this from EventFactory.
        self.result = name      # the name of the result (e.g., "win", "loss", etc)
        self.score = score      # a tuple of scores (Home, Away)

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.result}, ({self.score}))"



class StatisticalResult(Result):
    """
	what happened after the event, e.g., TeamA has win/loss/tie/....
	a series of all possible (nonzero probability) results are generated, with probabilities attached to each.
	"""

    def __init__(self, e, name: str, score: tuple=None, p: float=None):
        self.this_event = e     # the 'parent' event, for which this is the result
        self.next_event = None  # the 'next' event: get this from EventFactory.
        self.result = name      # the name of the result (e.g., "win", "loss", etc)
        self.probability = p    # the probability of this result

    def __repr__(self):
        return f"{self.__class__.__name__}: ({self.result}, {self.probability})"

