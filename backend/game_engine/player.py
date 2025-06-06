from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

try:
    from . import constants
except ImportError:  # pragma: no cover - constants may not be defined yet
    constants = None  # type: ignore


@dataclass
class Player:
    """Represents the director/player and stores career data."""

    name: str
    reputation: int = 10
    network_influence: int = 0
    genre_strengths: Dict[str, int] = field(default_factory=dict)
    past_projects: List[Dict] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.reputation = max(0, min(100, self.reputation))

    def add_project(self, project: Dict) -> None:
        """Record a completed project."""
        self.past_projects.append(project)

    def update_genre_strength(self, genre: str, delta: int) -> None:
        """Update the score for a given genre."""
        self.genre_strengths[genre] = self.genre_strengths.get(genre, 0) + delta

    def adjust_reputation(self, delta: int) -> None:
        """Adjust reputation within the 0-100 bounds."""
        self.reputation = max(0, min(100, self.reputation + delta))

    def get_profile_summary(self) -> Dict[str, object]:
        """Return key summary data about the player."""
        return {
            "name": self.name,
            "reputation": self.reputation,
            "genre_strengths": self.genre_strengths,
            "projects_completed": len(self.past_projects),
        }
