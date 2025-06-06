"""Logic for evaluating a project's release success.

This module provides functions used once a project has been completed. It
computes public and critical response, financial success and award
potential. The functions here are intentionally self contained so they can
be reused across any interface or front end for the game.
"""
from __future__ import annotations

import random
from typing import Any, Dict, List

from .constants import AWARDS

# Basic type alias for cast members. A full Talent class may exist in the
# actual game code base, but the logic here only relies on a ``star_power``
# attribute if present.
Talent = Any


def _clamp(value: int, min_value: int = 0, max_value: int = 100) -> int:
    """Clamp ``value`` between ``min_value`` and ``max_value``."""
    return max(min_value, min(max_value, value))


def evaluate_awards(project: Dict[str, Any], critics_score: int, fan_score: int) -> List[str]:
    """Return a list of awards won by the project.

    Parameters
    ----------
    project:
        Dictionary describing the finished project.
    critics_score:
        Final critic score for the project.
    fan_score:
        Final audience score for the project.

    Returns
    -------
    list[str]
        A list of award names that the project wins.
    """

    awards: List[str] = []

    # Basic threshold based on critics score.
    if critics_score >= 85:
        awards.append("Best Picture")

        # Extra awards for player written or particularly risky projects.
        if project.get("player_written"):
            awards.append("Best Screenplay")
        if project.get("risk_factor", 0) > 7:
            awards.append("Best Director")

    # Small chance for acting awards if the fan response was also high
    if fan_score > 80 and random.random() < 0.3:
        awards.extend(["Best Actor", "Best Actress"])

    # Filter awards so they only contain valid entries from constants.py and
    # remove duplicates while preserving order.
    unique_awards = []
    for a in awards:
        if a in AWARDS and a not in unique_awards:
            unique_awards.append(a)

    return unique_awards


def evaluate_release(project: Dict[str, Any], quality_score: int, cast: List[Talent]) -> Dict[str, Any]:
    """Evaluate the final release of a project.

    This function simulates how critics and audiences react to the finished
    project and estimates its financial success. Random modifiers are used to
    reflect the inherent unpredictability of entertainment releases.

    Parameters
    ----------
    project:
        Dictionary representing the completed project.
    quality_score:
        Numerical score returned from the production simulation.
    cast:
        List of cast members. Each member may optionally define a
        ``star_power`` attribute which influences box office.

    Returns
    -------
    dict
        Dictionary containing release statistics. Keys include ``critics_score``,
        ``fan_score``, ``box_office`` (or ``viewership`` for TV projects),
        ``awards``, ``profit`` and ``award_nominations``.
    """

    # Critics score is heavily influenced by the quality score with a small
    # random variance.
    critics_variance = random.randint(-5, 5)
    critics_score = _clamp(quality_score + critics_variance)

    # Fans can react differently. Start from the critics score and add a larger
    # random swing to represent broader audience taste.
    fan_variance = random.randint(-15, 15)
    fan_score = _clamp(critics_score + fan_variance)

    # Determine overall star power of the cast. Default to 50 if no attribute is
    # present so unknown actors still contribute a moderate amount.
    if cast:
        total_star_power = sum(getattr(member, "star_power", 50) for member in cast)
        average_star_power = total_star_power / len(cast)
    else:
        average_star_power = 50

    # Box office or viewership is loosely based on audience score and the star
    # power of the cast, then modified randomly.
    performance_factor = (fan_score / 100) * (average_star_power / 50)
    randomness = random.uniform(0.8, 1.2)

    if project.get("type") == "tv":
        # For television projects we estimate viewership numbers instead of box
        # office. The scale here is arbitrary but consistent within the game.
        base = project.get("episodes", 1) * 100_000
        box_office = int(base * performance_factor * randomness)
    else:
        base = 10_000_000  # baseline for film releases
        box_office = int(base * performance_factor * randomness)

    budget = project.get("budget", 0)
    profit = box_office - budget

    # Determine award wins and nominations.
    awards = evaluate_awards(project, critics_score, fan_score)

    # Nominations occur at a slightly lower threshold than wins.
    award_nominations = []
    if critics_score > 75:
        nomination_pool = [a for a in AWARDS if a not in awards]
        num_noms = min(len(nomination_pool), random.randint(1, 3))
        award_nominations.extend(random.sample(nomination_pool, num_noms))

    return {
        "critics_score": critics_score,
        "fan_score": fan_score,
        "box_office": box_office,
        "awards": awards,
        "profit": profit,
        "award_nominations": award_nominations,
    }
