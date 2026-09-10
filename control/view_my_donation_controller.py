from typing import List
from entity.donation import donation

class view_my_donation_controller:
    """
    Control class responsible for retrieving my donation details.
    """

    def viewMyDonations(self, account_id: int) -> List["donation"]:
        """
        Retrieve all donation object for the given account_id.
        """
        return donation.viewMyDonations(account_id)