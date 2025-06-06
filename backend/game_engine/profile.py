from __future__ import annotations

from typing import TYPE_CHECKING, List, Dict, Any, Optional, Set

if TYPE_CHECKING:
    # Placeholder import for type checking. The actual Player class
    # should define a ``past_projects`` attribute used here.
    from .player import Player


def add_completed_project(player: 'Player', project_data: Dict[str, Any]) -> None:
    """Append a completed project record to ``player.past_projects``.

    The record is stored with a placeholder ``poster_url`` field if one is not
    provided. ``player`` is expected to have a ``past_projects`` attribute that
    behaves like a list.
    """
    if not hasattr(player, "past_projects"):
        player.past_projects = []  # type: ignore[attr-defined]

    project = dict(project_data)
    project.setdefault("poster_url", None)

    player.past_projects.append(project)  # type: ignore[attr-defined]


def get_profile_summary(player: 'Player') -> Dict[str, Any]:
    """Return a dictionary summarizing the player's completed projects.

    The summary includes overall statistics and simplified information about
    each project for display on a public profile page.
    """
    projects: List[Dict[str, Any]] = getattr(player, "past_projects", [])  # type: ignore[attr-defined]

    total_projects = len(projects)
    total_critics = 0.0
    total_fans = 0.0
    awards: Set[Any] = set()

    use_box_office = any("box_office" in p for p in projects)
    use_viewership = not use_box_office and any("viewership" in p for p in projects)

    total_box_office = 0.0
    total_viewership = 0.0

    highest_grossing: Optional[Dict[str, Any]] = None
    highest_amount = -1.0

    summaries: List[Dict[str, Any]] = []

    for p in projects:
        critics_score = float(p.get("critics_score", 0) or 0)
        fan_score = float(p.get("fan_score", 0) or 0)
        total_critics += critics_score
        total_fans += fan_score

        if use_box_office:
            amount = float(p.get("box_office", 0) or 0)
            total_box_office += amount
        elif use_viewership:
            amount = float(p.get("viewership", 0) or 0)
            total_viewership += amount
        else:
            amount = 0.0

        if amount > highest_amount:
            highest_amount = amount
            highest_grossing = p

        for award in p.get("awards", []):
            awards.add(award)

        summaries.append({
            "title": p.get("title"),
            "year": p.get("year"),
            "medium": p.get("medium"),
            "genre": p.get("genre"),
            "poster_url": p.get("poster_url"),
        })

    avg_critics = total_critics / total_projects if total_projects else 0.0
    avg_fans = total_fans / total_projects if total_projects else 0.0

    summary: Dict[str, Any] = {
        "total_projects": total_projects,
        "average_critics_score": avg_critics,
        "average_fan_score": avg_fans,
        "awards_won": sorted(awards),
        "highest_grossing_project": highest_grossing,
        "projects": summaries,
    }

    if use_box_office:
        summary["total_box_office"] = total_box_office
    elif use_viewership:
        summary["total_viewership"] = total_viewership
    else:
        summary["total_box_office"] = 0.0

    return summary
