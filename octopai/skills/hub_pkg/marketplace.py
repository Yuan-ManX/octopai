"""
Marketplace Manager - Ratings, reviews, and marketplace features for Skills Hub.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class RatingType(str, Enum):
    """Types of ratings."""
    OVERALL = "overall"
    DOCUMENTATION = "documentation"
    USABILITY = "usability"
    PERFORMANCE = "performance"
    RELIABILITY = "reliability"


@dataclass
class Rating:
    """User rating for a skill repository.

    Attributes:
        id: Unique rating identifier
        repo_id: Repository being rated
        user_id: User providing the rating
        scores: Dictionary of rating type to score (1-5)
        overall_score: Calculated overall score
        comment: Optional text comment
        created_at: When the rating was created
        updated_at: When the rating was last updated
        is_verified: Whether from verified purchaser/user
        helpful_count: Number of users who found this helpful
    """

    id: str = ""
    repo_id: str = ""
    user_id: str = ""
    scores: Dict[str, int] = field(default_factory=dict)
    overall_score: float = 0.0
    comment: str = ""
    created_at: str = ""
    updated_at: str = ""
    is_verified: bool = False
    helpful_count: int = 0

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()
        if not self.scores:
            self.scores = {RatingType.OVERALL.value: 3}
        if not self.overall_score:
            self.overall_score = self._calculate_overall()

    def _calculate_overall(self) -> float:
        """Calculate weighted average of all scores."""
        if not self.scores:
            return 0.0

        weights = {
            RatingType.OVERALL.value: 1.0,
            RatingType.DOCUMENTATION.value: 1.0,
            RatingType.USABILITY.value: 1.2,
            RatingType.PERFORMANCE.value: 1.3,
            RatingType.RELIABILITY.value: 1.4,
        }

        total_weight = 0.0
        weighted_sum = 0.0

        for rating_type, score in self.scores.items():
            weight = weights.get(rating_type, 1.0)
            weighted_sum += score * weight
            total_weight += weight

        return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0


@dataclass
class Review:
    """Detailed review with text and analysis.

    Attributes:
        id: Unique review identifier
        repo_id: Repository being reviewed
        user_id: User writing the review
        title: Review title
        content: Detailed review text (markdown)
        pros: List of positive points
        cons: List of negative points
        rating_id: Associated rating ID
        created_at: When written
        updated_at: Last update time
        is_featured: Whether this is a featured review
        response_from_author: Author's response (if any)
        upvotes: Number of upvotes
        downvotes: Number of downvotes
    """

    id: str = ""
    repo_id: str = ""
    user_id: str = ""
    title: str = ""
    content: str = ""
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    rating_id: str = ""
    created_at: str = ""
    updated_at: str = ""
    is_featured: bool = False
    response_from_author: str = ""
    upvotes: int = 0
    downvotes: int = 0


@dataclass
class AggregatedRatings:
    """Aggregated rating statistics for a repository.

    Attributes:
        repo_id: Repository ID
        average_scores: Average score per category
        overall_average: Weighted overall average
        total_ratings: Total number of ratings
        distribution: Score distribution (1-5 stars counts)
        recent_average: Average of last N ratings
        verified_average: Average from verified users only
    """

    repo_id: str = ""
    average_scores: Dict[str, float] = field(default_factory=dict)
    overall_average: float = 0.0
    total_ratings: int = 0
    distribution: Dict[int, int] = field(default_factory=lambda: {i: 0 for i in range(1, 6)})
    recent_average: float = 0.0
    verified_average: float = 0.0


@dataclass
class TrendingSkill:
    """Information about a trending skill.

    Attributes:
        repo_id: Repository ID
        name: Skill name
        current_rank: Current trending rank
        previous_rank: Previous rank (for change indicator)
        score_change: Change in score/engagement
        period: Time period for this trend
    """

    repo_id: str = ""
    name: str = ""
    current_rank: int = 0
    previous_rank: int = 0
    score_change: float = 0.0
    period: str = "week"


class MarketplaceManager:
    """Manages marketplace features for Skills Hub.

    Handles:
    - User ratings and reviews
    - Aggregated statistics
    - Trending skills
    - Recommendations
    - Quality scoring
    """

    def __init__(self):
        """Initialize marketplace manager."""
        self.ratings: Dict[str, List[Rating]] = {}
        self.reviews: Dict[str, List[Review]] = {}

    def add_rating(
        self,
        repo_id: str,
        user_id: str,
        scores: Dict[str, int],
        comment: str = "",
        is_verified: bool = False,
    ) -> Rating:
        """Add or update a user's rating.

        Args:
            repo_id: Repository being rated
            user_id: User providing rating
            scores: Dictionary of category to score (1-5)
            comment: Optional comment
            is_verified: Whether from verified user

        Returns:
            Created/updated Rating object
        """
        import uuid

        existing = self._find_user_rating(repo_id, user_id)

        if existing:
            existing.scores = scores
            existing.comment = comment
            existing.is_verified = is_verified
            existing.updated_at = datetime.now().isoformat()
            existing.overall_score = existing._calculate_overall()
            return existing

        rating = Rating(
            id=str(uuid.uuid4()),
            repo_id=repo_id,
            user_id=user_id,
            scores=scores,
            comment=comment,
            is_verified=is_verified,
        )

        if repo_id not in self.ratings:
            self.ratings[repo_id] = []

        self.ratings[repo_id].append(rating)

        return rating

    def get_rating(self, repo_id: str, user_id: str) -> Optional[Rating]:
        """Get a specific user's rating.

        Args:
            repo_id: Repository ID
            user_id: User ID

        Returns:
            Rating or None if not found
        """
        return self._find_user_rating(repo_id, user_id)

    def remove_rating(self, repo_id: str, user_id: str) -> bool:
        """Remove a user's rating.

        Args:
            repo_id: Repository ID
            user_id: User ID

        Returns:
            True if removed successfully
        """
        if repo_id not in self.ratings:
            return False

        original_len = len(self.ratings[repo_id])
        self.ratings[repo_id] = [
            r for r in self.ratings[repo_id]
            if r.user_id != user_id
        ]

        return len(self.ratings[repo_id]) < original_len

    def get_aggregated_ratings(self, repo_id: str) -> AggregatedRatings:
        """Get aggregated rating statistics for a repository.

        Args:
            repo_id: Repository ID

        Returns:
            AggregatedRatings with full statistics
        """
        ratings = self.ratings.get(repo_id, [])

        if not ratings:
            return AggregatedRatings(
                repo_id=repo_id,
                average_scores={},
                overall_average=0.0,
                total_ratings=0,
            )

        avg_scores: Dict[str, float] = {}
        all_categories = set()

        for r in ratings:
            all_categories.update(r.scores.keys())

        for cat in all_categories:
            values = [r.scores.get(cat, 0) for r in ratings if cat in r.scores]
            if values:
                avg_scores[cat] = round(sum(values) / len(values), 2)

        overall_avg = sum(r.overall_score for r in ratings) / len(ratings)

        distribution: Dict[int, int] = {i: 0 for i in range(1, 6)}
        for r in ratings:
            score_int = int(round(r.overall_score))
            score_int = max(1, min(5, score_int))
            distribution[score_int] += 1

        recent = sorted(ratings, key=lambda r: r.created_at, reverse=True)[:10]
        recent_avg = sum(r.overall_score for r in recent) / len(recent) if recent else 0.0

        verified = [r for r in ratings if r.is_verified]
        verified_avg = sum(r.overall_score for r in verified) / len(verified) if verified else 0.0

        return AggregatedRatings(
            repo_id=repo_id,
            average_scores=avg_scores,
            overall_average=round(overall_avg, 2),
            total_ratings=len(ratings),
            distribution=distribution,
            recent_average=round(recent_avg, 2),
            verified_average=round(verified_avg, 2),
        )

    def add_review(
        self,
        repo_id: str,
        user_id: str,
        title: str,
        content: str,
        pros: List[str],
        cons: List[str],
        rating_id: str = "",
    ) -> Review:
        """Add a detailed review.

        Args:
            repo_id: Repository ID
            user_id: User ID
            title: Review title
            content: Review content (markdown)
            pros: Positive points
            cons: Negative points
            rating_id: Associated rating ID

        Returns:
            Created Review object
        """
        import uuid

        review = Review(
            id=str(uuid.uuid4()),
            repo_id=repo_id,
            user_id=user_id,
            title=title,
            content=content,
            pros=pros,
            cons=cons,
            rating_id=rating_id,
        )

        if repo_id not in self.reviews:
            self.reviews[repo_id] = []

        self.reviews[repo_id].append(review)

        return review

    def get_reviews(
        self,
        repo_id: str,
        limit: int = 20,
        sort_by: str = "helpful",
    ) -> List[Review]:
        """Get reviews for a repository.

        Args:
            repo_id: Repository ID
            limit: Max results
            sort_by: Sort method ("helpful", "recent", "rating")

        Returns:
            List of Review objects
        """
        reviews = self.reviews.get(repo_id, [])

        if sort_by == "helpful":
            reviews.sort(key=lambda r: r.upvotes, reverse=True)
        elif sort_by == "recent":
            reviews.sort(key=lambda r: r.created_at, reverse=True)
        elif sort_by == "rating":
            reviews.sort(key=lambda r: self._get_review_rating(r), reverse=True)

        return reviews[:limit]

    def get_trending_skills(
        self,
        hub_manager=None,
        period: str = "week",
        limit: int = 10,
    ) -> List[TrendingSkill]:
        """Get currently trending skills.

        Args:
            hub_manager: HubManager instance for additional data
            period: Time period ("day", "week", "month")
            limit: Max results

        Returns:
            List of TrendingSkill objects
        """
        if not hub_manager:
            return []

        popular = hub_manager.get_popular_repositories(limit * 3)

        trending = []
        for i, repo in enumerate(popular[:limit]):
            agg = self.get_aggregated_ratings(repo.id)

            trend = TrendingSkill(
                repo_id=repo.id,
                name=repo.display_name or repo.name,
                current_rank=i + 1,
                previous_rank=i + 1,
                score_change=agg.overall_average * 10,
                period=period,
            )
            trending.append(trend)

        return sorted(trending, key=lambda t: t.score_change, reverse=True)[:limit]

    def get_recommendations(
        self,
        user_id: str,
        hub_manager=None,
        limit: int = 10,
    ) -> List[tuple]:
        """Get personalized recommendations for a user.

        Args:
            user_id: User ID
            hub_manager: HubManager instance
            limit: Max results

        Returns:
            List of (repository, relevance_score) tuples
        """
        if not hub_manager:
            return []

        user_rated_ids = set()
        for repo_id, ratings in self.ratings.items():
            for r in ratings:
                if r.user_id == user_id:
                    user_rated_ids.add(repo_id)

        unrated_public = [
            r for r in hub_manager.list_repositories(visibility="public")
            if r.id not in user_rated_ids
        ]

        recommendations = []
        for repo in unrated_public[:limit * 2]:
            agg = self.get_aggregated_ratings(repo.id)
            relevance = (
                agg.overall_average * 0.6 +
                min(repo.stars / 100, 1.0) * 0.3 +
                min(len(repo.contributors) / 10, 1.0) * 0.1
            )
            recommendations.append((repo, relevance))

        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations[:limit]

    def mark_helpful(self, review_id: str, user_id: str) -> bool:
        """Mark a review as helpful.

        Args:
            review_id: Review ID
            user_id: User marking as helpful

        Returns:
            True if successful
        """
        for repo_reviews in self.reviews.values():
            for review in repo_reviews:
                if review.id == review_id:
                    review.helpful_count += 1
                    return True
        return False

    def _find_user_rating(self, repo_id: str, user_id: str) -> Optional[Rating]:
        """Find existing rating by user on repository."""
        if repo_id not in self.ratings:
            return None

        for r in self.ratings[repo_id]:
            if r.user_id == user_id:
                return r

        return None

    def _get_review_rating(self, review: Review) -> float:
        """Get associated rating score for a review."""
        if not review.rating_id:
            return 0.0

        for repo_id, ratings in self.ratings.items():
            for r in ratings:
                if r.id == review.rating_id:
                    return r.overall_score

        return 0.0
