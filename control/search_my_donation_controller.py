from typing import Tuple, Optional
from entity.donation import donation


class search_my_donation_controller:
    """
    Control class responsible for searching my donations.
    """
    def searchMyDonations(self, account_id: int, searchTerm: str, categoryId: str = "", dateFrom: str = "", dateTo: str = "", amountMin: str = "", amountMax: str = "") -> Optional["donation"]:
        return donation.searchMyDonations(account_id, searchTerm, categoryId, dateFrom, dateTo, amountMin, amountMax)