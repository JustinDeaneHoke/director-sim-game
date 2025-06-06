import random
from typing import List, Dict


def generate_offer_list() -> List[Dict]:
    """Generate a list of mock project offers."""
    offers = []
    for i in range(1, 4):
        offers.append(
            {
                "id": i,
                "title": f"Project {i}",
                "budget": random.randint(1_000_000, 5_000_000),
            }
        )
    return offers
