"""
Frontier Manager - Manages the set of top-performing skill variants.

The frontier maintains the best-performing variants discovered during evolution,
allowing selection of parents for future mutations and tracking overall progress.
"""

import json
import random
from pathlib import Path
from typing import Optional

from .config import SkillVariant, SelectionStrategy


class FrontierManager:
    """Manages the frontier of top-performing skill variants.

    The frontier is a fixed-size collection of the best-performing variants.
    When a new variant outperforms the worst member, it replaces it.

    Attributes:
        max_size: Maximum number of variants to keep in frontier
        variants: Dictionary mapping variant names to SkillVariant objects
    """

    def __init__(self, max_size: int = 5):
        """Initialize frontier manager.

        Args:
            max_size: Maximum number of variants in frontier
        """
        self.max_size = max_size
        self.variants: dict[str, SkillVariant] = {}

    def add(self, variant: SkillVariant) -> bool:
        """Attempt to add a variant to the frontier.

        A variant is added if:
        - Frontier has room (size < max_size), OR
        - Variant's score exceeds the lowest score in frontier

        Args:
            variant: Variant to add

        Returns:
            True if variant was added, False otherwise
        """
        if len(self.variants) < self.max_size:
            self.variants[variant.name] = variant
            return True

        if not self.variants:
            self.variants[variant.name] = variant
            return True

        worst_name = self._get_worst_name()
        worst_score = self.variants[worst_name].score

        if variant.score > worst_score:
            del self.variants[worst_name]
            self.variants[variant.name] = variant
            return True

        return False

    def remove(self, name: str) -> bool:
        """Remove a variant from the frontier.

        Args:
            name: Name of variant to remove

        Returns:
            True if variant was removed, False if not found
        """
        if name in self.variants:
            del self.variants[name]
            return True
        return False

    def get_best(self) -> Optional[SkillVariant]:
        """Get the best-performing variant.

        Returns:
            Best SkillVariant or None if frontier is empty
        """
        if not self.variants:
            return None

        return max(self.variants.values(), key=lambda v: v.score)

    def get_best_name(self) -> str:
        """Get name of best-performing variant.

        Returns:
            Name of best variant or empty string if frontier empty
        """
        best = self.get_best()
        return best.name if best else ""

    def get_worst(self) -> Optional[SkillVariant]:
        """Get the worst-performing variant.

        Returns:
            Worst SkillVariant or None if frontier is empty
        """
        if not self.variants:
            return None

        return min(self.variants.values(), key=lambda v: v.score)

    def _get_worst_name(self) -> str:
        """Get name of worst-performing variant."""
        worst = self.get_worst()
        return worst.name if worst else ""

    def get_sorted(self) -> list[tuple[str, float]]:
        """Get all variants sorted by score descending.

        Returns:
            List of (name, score) tuples sorted by score
        """
        return sorted(
            [(name, v.score) for name, v in self.variants.items()],
            key=lambda x: x[1],
            reverse=True,
        )

    def select_parent(
        self,
        strategy: SelectionStrategy = SelectionStrategy.BEST,
        iteration: int = 0,
    ) -> Optional[str]:
        """Select a parent variant using specified strategy.

        Args:
            strategy: Selection strategy to use
            iteration: Current iteration number (for round_robin)

        Returns:
            Selected parent name or None if frontier empty
        """
        if not self.variants:
            return None

        sorted_variants = self.get_sorted()

        if strategy == SelectionStrategy.BEST:
            return sorted_variants[0][0]

        elif strategy == SelectionStrategy.RANDOM:
            return random.choice(sorted_variants)[0]

        elif strategy == SelectionStrategy.ROUND_ROBIN:
            index = iteration % len(sorted_variants)
            return sorted_variants[index][0]

        else:
            return sorted_variants[0][0]

    def contains(self, name: str) -> bool:
        """Check if a variant is in the frontier.

        Args:
            name: Variant name to check

        Returns:
            True if variant exists in frontier
        """
        return name in self.variants

    def get(self, name: str) -> Optional[SkillVariant]:
        """Get a specific variant by name.

        Args:
            name: Variant name

        Returns:
            SkillVariant or None if not found
        """
        return self.variants.get(name)

    def size(self) -> int:
        """Get current size of frontier."""
        return len(self.variants)

    def is_full(self) -> bool:
        """Check if frontier is at maximum capacity."""
        return len(self.variants) >= self.max_size

    def clear(self) -> None:
        """Clear all variants from frontier."""
        self.variants.clear()

    def get_average_score(self) -> float:
        """Calculate average score of all frontier variants.

        Returns:
            Average score or 0.0 if frontier empty
        """
        if not self.variants:
            return 0.0

        total = sum(v.score for v in self.variants.values())
        return total / len(self.variants)

    def get_score_range(self) -> tuple[float, float]:
        """Get range of scores in frontier.

        Returns:
            Tuple of (min_score, max_score)
        """
        if not self.variants:
            return (0.0, 0.0)

        scores = [v.score for v in self.variants.values()]
        return (min(scores), max(scores))

    def get_statistics(self) -> dict:
        """Get comprehensive statistics about the frontier.

        Returns:
            Dictionary with frontier statistics
        """
        if not self.variants:
            return {
                "size": 0,
                "average_score": 0.0,
                "best_score": 0.0,
                "worst_score": 0.0,
                "score_range": (0.0, 0.0),
                "generations": [],
            }

        scores = [v.score for v in self.variants.values()]
        generations = [v.generation for v in self.variants.values()]

        return {
            "size": len(self.variants),
            "average_score": sum(scores) / len(scores),
            "best_score": max(scores),
            "worst_score": min(scores),
            "score_range": (min(scores), max(scores)),
            "generations": generations,
            "names": list(self.variants.keys()),
        }

    def save_to_file(self, path: Path) -> None:
        """Save frontier state to file.

        Args:
            path: Path to save frontier data
        """
        data = {
            "max_size": self.max_size,
            "variants": {
                name: {
                    "name": v.name,
                    "content": v.content,
                    "score": v.score,
                    "generation": v.generation,
                    "parent": v.parent,
                    "mutations": v.mutations,
                    "metadata": v.metadata,
                }
                for name, v in self.variants.items()
            },
        }

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self, path: Path) -> bool:
        """Load frontier state from file.

        Args:
            path: Path to load frontier data from

        Returns:
            True if loaded successfully, False otherwise
        """
        if not path.exists():
            return False

        try:
            with open(path, 'r') as f:
                data = json.load(f)

            self.max_size = data.get("max_size", self.max_size)
            self.variants = {}

            for name, v_data in data.get("variants", {}).items():
                self.variants[name] = SkillVariant(
                    name=v_data["name"],
                    content=v_data["content"],
                    score=v_data.get("score", 0.0),
                    generation=v_data.get("generation", 0),
                    parent=v_data.get("parent"),
                    mutations=v_data.get("mutations", []),
                    metadata=v_data.get("metadata", {}),
                )

            return True

        except Exception as e:
            print(f"Failed to load frontier: {e}")
            return False

    def __len__(self) -> int:
        """Return current frontier size."""
        return len(self.variants)

    def __contains__(self, name: str) -> bool:
        """Check if variant exists in frontier."""
        return name in self.variants

    def __iter__(self):
        """Iterate over frontier variants."""
        return iter(self.variants.values())

    def __repr__(self) -> str:
        """String representation of frontier."""
        return f"FrontierManager(size={len(self.variants)}/{self.max_size})"
