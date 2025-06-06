"""Production simulation module for film/TV/commercial projects."""

from __future__ import annotations

import random
from typing import List, Dict, Any

# Placeholder import for Talent type hinting
try:
    from casting import Talent
except ImportError:  # pragma: no cover - casting module may not exist in this repo
    class Talent:  # type: ignore
        skill: int = 0


def log_event(event: str, notes: List[str]) -> None:
    """Internal helper to append an event to production notes."""
    notes.append(event)


def generate_random_production_events() -> List[str]:
    """Randomly select 1-3 production issues from a curated list."""
    possible_issues = [
        "Actor temper tantrum",
        "Crew illness",
        "Location flooded",
        "Network demands rewrites",
    ]
    return random.sample(possible_issues, k=random.randint(1, 3))


def apply_player_decisions(decisions: Dict[str, Any] | None) -> Dict[str, int]:
    """Apply player decisions to production results.

    Currently returns basic modifiers; future versions may expand on this.
    """
    decisions = decisions or {}
    modifiers = {"quality": 0, "delay": 0}

    if decisions.get("extra_rehearsal"):
        modifiers["quality"] += 5
    if decisions.get("rush_schedule"):
        modifiers["quality"] -= 5
        modifiers["delay"] -= 1  # negative delay means faster

    return modifiers


def simulate_production(project: Dict[str, Any], cast: List[Talent]) -> Dict[str, Any]:
    """Simulate the active production phase of a project.

    Parameters
    ----------
    project : dict
        Dictionary describing the project. Expected key ``base_quality`` may be
        used to seed the quality calculation.
    cast : list[``Talent``]
        List of cast members involved in the production.
    """

    base_quality = project.get("base_quality", 50)
    quality = base_quality
    production_notes: List[str] = []
    issues: List[str] = []
    delay_weeks = 0

    # Apply random production events
    events = generate_random_production_events()
    for event in events:
        log_event(f"Issue encountered: {event}", production_notes)
        issues.append(event)
        quality -= random.randint(5, 15)
        delay_weeks += random.randint(0, 2)

    # Cap delays between 0 and 5 weeks
    delay_weeks = min(max(delay_weeks, 0), 5)

    # Incorporate cast skill
    cast_skill = sum(getattr(member, "skill", 0) for member in cast)
    quality += cast_skill

    # Apply player decisions if present in project data
    decision_mods = apply_player_decisions(project.get("decisions"))
    quality += decision_mods.get("quality", 0)
    delay_weeks += decision_mods.get("delay", 0)
    delay_weeks = min(max(delay_weeks, 0), 5)

    final_quality_score = quality

    # Possible studio feedback
    feedback_options = [
        "All good – proceed to post production!",
        "Studio requests a happier ending",
        "Studio wants reshoots",
        "Studio is thrilled with the footage",
    ]
    studio_feedback = random.choice(feedback_options)

    return {
        "final_quality_score": final_quality_score,
        "delays": delay_weeks,
        "issues": issues,
        "production_notes": production_notes,
        "studio_feedback": studio_feedback,
    }
