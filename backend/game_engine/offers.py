import random
from typing import List, Dict

from .constants import GENRES, ROLES


def generate_offer_list() -> List[Dict]:
    """Generate a list of mock project offers.

    Each offer contains the basic project data expected by the front end. The
    values are intentionally simple/randomised to keep the function lightweight
    and dependency free.
    """

    offers: List[Dict] = []

    mediums = list(GENRES.keys())
    role_choices = [r for r in ROLES if r != "director"]

    for i in range(1, 4):
        medium = random.choice(mediums)
        genre = random.choice(GENRES[medium])

        # Select a handful of roles that need to be cast. Always include lead
        # and supporting actor so the UI has something to request.
        roles = ["lead actor", "supporting actor"]
        others = [r for r in role_choices if r not in roles]
        random.shuffle(others)
        roles.extend(others[:2])

        offer = {
            "id": i,
            "title": f"Project {i}",
            "budget": random.randint(1_000_000, 5_000_000),
            "genre": genre,
            "medium": medium,
            "roles": roles,
            "tagline": f"A {genre} {medium} experience",
            # ``risk`` doubles as the risk factor used later in release logic
            "risk": random.randint(1, 10),
        }

        # Mirror ``risk`` under ``risk_factor`` for internal use
        offer["risk_factor"] = offer["risk"]

        offers.append(offer)

    return offers
