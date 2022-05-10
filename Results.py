
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

    def increment(self, result: str, amount: int)->int:
        # increments the particular result
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

    def __init__(self, e, name: str, score: tuple=None, p: float=None):
        self.this_event = e     # the 'parent' event, for which this is the result
        self.next_event = None  # the 'next' event: get this from EventFactory.
        self.result = name      # the name of the result (e.g., "win", "loss", etc)
        self.score = score      # a tuple of scores (Home, Away)
        self.probability = p    # the probability of this result

