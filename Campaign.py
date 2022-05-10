# manages the campaign
# check when the campaign is over
from Events import Event

class CampaignException(BaseException):
    pass


class Campaign:
    def __init__(self, details: dict):
        self._details = details

    def is_finished(self, leaf_node: Event)->bool:
        # return True if the campaign is over and False otherwise
        campaign_count = leaf_node.get_campaign_count()
        try:
            camp_type = self._details["campaign"]["type"]
            camp_length = self._details["campaign"]["length"]
            if camp_type == "best-of-series":
                pass
            elif camp_type == "fixed-series":
                if campaign_count >= camp_length:
                    return False
            else:
                raise CampaignException(f"unrecognized campaign type: {camp_type}")
        except KeyError as ke:
            raise CampaignException(f"campaign details missing expected key(s): {self._details["campaign"]}")

