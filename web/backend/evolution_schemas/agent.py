"""
Agent Response Schema
Schema for agent responses
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class AgentResponse:
    """Response from an agent"""
    final_answer: str
    reasoning: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "final_answer": self.final_answer,
            "reasoning": self.reasoning,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentResponse":
        """Create from dictionary"""
        return cls(
            final_answer=data.get("final_answer", ""),
            reasoning=data.get("reasoning", ""),
            metadata=data.get("metadata", {})
        )
