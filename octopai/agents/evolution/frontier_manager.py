"""
Frontier Management System
Manages multiple evolution directions with intelligent selection
"""

from typing import List, Optional, Dict, Any
from datetime import datetime


class FrontierManager:
    """Manages multiple evolution directions with frontier selection"""

    def __init__(self, max_frontier_size: int = 5):
        self.max_size = max_frontier_size
        self.frontier: List[Dict[str, Any]] = []
        self.selection_strategies = ['best', 'random', 'round_robin']
        self.current_round_robin_idx = 0

    def add_candidate(self, candidate_id: str, score: float, 
                     metadata: Dict[str, Any] = None) -> bool:
        """Add a candidate to frontier if it qualifies"""
        candidate = {
            'candidate_id': candidate_id,
            'score': round(score, 4),
            'metadata': metadata or {},
            'added_at': datetime.now().isoformat()
        }
        
        if len(self.frontier) < self.max_size:
            self.frontier.append(candidate)
            self._sort_frontier()
            return True
        
        worst_score = self.frontier[-1]['score'] if self.frontier else 0
        
        if score > worst_score:
            self.frontier.pop()
            self.frontier.append(candidate)
            self._sort_frontier()
            return True
        
        return False

    def _sort_frontier(self):
        self.frontier.sort(key=lambda x: x['score'], reverse=True)

    def select_candidate(self, strategy: str = 'best', 
                        iteration: int = 0) -> Optional[Dict]:
        """Select a candidate from frontier using specified strategy"""
        if not self.frontier:
            return None
        
        if strategy == 'random':
            return random.choice(self.frontier)
        elif strategy == 'round_robin':
            selected = self.frontier[self.current_round_robin_idx % len(self.frontier)]
            self.current_round_robin_idx += 1
            return selected
        else:
            return self.frontier[0]

    def get_best(self) -> Optional[Dict]:
        return self.frontier[0] if self.frontier else None

    def get_all_sorted(self) -> List[Dict]:
        return sorted(self.frontier, key=lambda x: x['score'], reverse=True)

    def remove_worst(self) -> Optional[Dict]:
        if self.frontier:
            return self.frontier.pop()
        return None

    def clear(self):
        self.frontier.clear()
        self.current_round_robin_idx = 0

    def get_stats(self) -> Dict[str, Any]:
        if not self.frontier:
            return {'size': 0, 'avg_score': 0, 'best_score': 0, 'worst_score': 0}
        
        scores = [c['score'] for c in self.frontier]
        return {
            'size': len(self.frontier),
            'avg_score': round(sum(scores) / len(scores), 3),
            'best_score': round(max(scores), 3),
            'worst_score': round(min(scores), 3),
            'diversity': round(self._calculate_diversity(), 3)
        }

    def _calculate_diversity(self) -> float:
        if len(self.frontier) < 2:
            return 1.0
        
        types = set()
        for c in self.frontier:
            meta_type = c.get('metadata', {}).get('type', 'unknown')
            types.add(meta_type)
        
        return len(types) / len(self.frontier)


import random
