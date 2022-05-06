# --------------------------------------------------------------------

class Result():
    """
	what happened after the event, e.g., TeamA has win/loss/tie/....
	"""

    def __init__(self, e: Event, name: str, p: float):
        self.thisevent = e      # the 'parent' event, for which this is the result
        self.nextevent = None   # the 'next' event: get this from EventFactory.
        self.name = name        # the name of the result (e.g., "win", "loss", etc)
        self.probability = p    # the probability of this result
