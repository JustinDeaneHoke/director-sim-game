from dataclasses import dataclass
from typing import List
import random

@dataclass
class Talent:
    """Represents an actor or crew member."""
    name: str
    role: str
    star_power: int  # affects box office
    skill: int       # affects final quality
    cost: int        # in dollars
    availability: bool
    working_relationship: float  # modifier based on past work with player
    wants_to_work_with_player: bool

# Placeholder reputation value until hooked into player profile
PLAYER_REPUTATION = 0.6  # 0 (terrible) - 1 (excellent)


def generate_talent_pool(role: str, count: int = 5) -> List[Talent]:
    """Return a list of potential actors/crew for the given role."""
    pool: List[Talent] = []
    for i in range(count):
        name = f"{role.title()} Talent {i + 1}"
        star_power = random.randint(0, 100)
        skill = random.randint(0, 100)
        base_cost = 10000
        cost = int(base_cost * (1 + star_power / 100) * (1 + skill / 200))
        availability = random.random() < 0.8
        working_relationship = random.uniform(-1.0, 1.0)
        willingness_chance = PLAYER_REPUTATION + working_relationship * 0.1
        willingness_chance = max(0.0, min(1.0, willingness_chance))
        wants_to_work = random.random() < willingness_chance

        pool.append(
            Talent(
                name=name,
                role=role,
                star_power=star_power,
                skill=skill,
                cost=cost,
                availability=availability,
                working_relationship=working_relationship,
                wants_to_work_with_player=wants_to_work,
            )
        )
    return pool


def evaluate_casting_choices(cast: List[Talent]) -> dict:
    """Aggregate the effects of a group of cast or crew choices."""
    if not cast:
        return {
            "expected_quality": 0.0,
            "box_office_boost": 0.0,
            "team_synergy_penalty": 0.0,
        }

    expected_quality = sum(t.skill for t in cast) / len(cast)
    box_office_boost = sum(t.star_power for t in cast) / len(cast)

    synergy_penalty = 0.0
    for t in cast:
        if not t.availability:
            synergy_penalty += 5.0
        if not t.wants_to_work_with_player:
            synergy_penalty += 5.0
        if t.working_relationship < 0:
            synergy_penalty += abs(t.working_relationship) * 10

    return {
        "expected_quality": expected_quality,
        "box_office_boost": box_office_boost,
        "team_synergy_penalty": synergy_penalty,
    }
