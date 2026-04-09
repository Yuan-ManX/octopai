"""
Program Manager
Manages program versions and the frontier
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from .models import ProgramConfig, ProgramMetadata


class ProgramManager:
    """
    Manages program versions and the frontier
    
    Programs are stored in a registry directory with:
    - Each program has a config file
    - Frontier tracks the top-performing programs
    """
    
    def __init__(self, registry_dir: Optional[str] = None):
        """
        Initialize the program manager
        
        Args:
            registry_dir: Directory to store program data
        """
        if registry_dir:
            self.registry_dir = Path(registry_dir)
        else:
            self.registry_dir = Path(".octopai") / "registry"
        
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.programs_dir = self.registry_dir / "programs"
        self.programs_dir.mkdir(parents=True, exist_ok=True)
        
        self._frontier_path = self.registry_dir / "frontier.json"
        self._current_program: Optional[str] = None
    
    def _get_program_path(self, name: str) -> Path:
        """Get path to a program's config file"""
        return self.programs_dir / f"{name}.json"
    
    def create_program(self, name: str, config: ProgramConfig, parent: Optional[str] = None) -> str:
        """
        Create a new program
        
        Args:
            name: Program name
            config: Program configuration
            parent: Optional parent program name
            
        Returns:
            Program name
        """
        # Set parent in metadata if provided
        if parent and not config.metadata.parent:
            config.metadata.parent = parent
        
        config.metadata.created_at = datetime.now().isoformat()
        
        # Save to file
        program_path = self._get_program_path(name)
        program_path.write_text(json.dumps(config.to_dict(), indent=2))
        
        return name
    
    def get_program(self, name: str) -> Optional[ProgramConfig]:
        """
        Get a program by name
        
        Args:
            name: Program name
            
        Returns:
            ProgramConfig or None if not found
        """
        program_path = self._get_program_path(name)
        if not program_path.exists():
            return None
        
        try:
            data = json.loads(program_path.read_text())
            return ProgramConfig.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading program {name}: {e}")
            return None
    
    def get_current(self) -> Optional[ProgramConfig]:
        """
        Get the currently active program
        
        Returns:
            Current ProgramConfig or None
        """
        if self._current_program:
            return self.get_program(self._current_program)
        return None
    
    def switch_to(self, name: str) -> bool:
        """
        Switch to a different program
        
        Args:
            name: Program name to switch to
            
        Returns:
            True if successful
        """
        if self.get_program(name) is not None:
            self._current_program = name
            return True
        return False
    
    def list_programs(self) -> List[str]:
        """
        List all program names
        
        Returns:
            List of program names
        """
        programs = []
        for program_file in self.programs_dir.glob("*.json"):
            programs.append(program_file.stem)
        return sorted(programs)
    
    def get_frontier(self) -> List[str]:
        """
        Get the current frontier (top-performing programs)
        
        Returns:
            List of program names in frontier
        """
        if not self._frontier_path.exists():
            return []
        
        try:
            data = json.loads(self._frontier_path.read_text())
            return [item[0] for item in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def get_frontier_with_scores(self) -> List[Tuple[str, float]]:
        """
        Get frontier with scores
        
        Returns:
            List of (name, score) tuples
        """
        if not self._frontier_path.exists():
            return []
        
        try:
            data = json.loads(self._frontier_path.read_text())
            return [(item[0], item[1]) for item in data]
        except (json.JSONDecodeError, KeyError):
            return []
    
    def update_frontier(self, program_name: str, score: float, max_size: int = 3) -> bool:
        """
        Update the frontier with a new program
        
        Args:
            program_name: Program to add
            score: Score of the program
            max_size: Maximum size of frontier
            
        Returns:
            True if program was added to frontier
        """
        # Update program's score
        program = self.get_program(program_name)
        if program:
            program.metadata.score = score
            self.create_program(program_name, program)
        
        # Get current frontier
        frontier = self.get_frontier_with_scores()
        
        # Add new entry
        frontier.append((program_name, score))
        
        # Sort by score descending
        frontier.sort(key=lambda x: x[1], reverse=True)
        
        # Trim to max size
        if len(frontier) > max_size:
            removed = frontier.pop()
            added = removed[0] != program_name
        else:
            added = True
        
        # Save frontier
        self._frontier_path.write_text(json.dumps(frontier, indent=2))
        
        return added
    
    def get_best_from_frontier(self) -> Optional[str]:
        """
        Get the best program from the frontier
        
        Returns:
            Best program name or None
        """
        frontier = self.get_frontier_with_scores()
        if frontier:
            return frontier[0][0]
        return None
    
    def select_from_frontier(self, strategy: str = "best", iteration: int = 0) -> Optional[str]:
        """
        Select a program from the frontier using a strategy
        
        Args:
            strategy: Selection strategy (best, random, round_robin)
            iteration: Iteration number for round_robin
            
        Returns:
            Selected program name or None
        """
        frontier = self.get_frontier()
        if not frontier:
            return None
        
        if strategy == "best":
            return frontier[0]
        elif strategy == "random":
            import random
            return random.choice(frontier)
        else:  # round_robin
            idx = (iteration - 1) % len(frontier)
            return frontier[idx]
    
    def discard(self, program_name: str) -> None:
        """
        Remove a program from the registry
        
        Args:
            program_name: Program to remove
        """
        program_path = self._get_program_path(program_name)
        if program_path.exists():
            program_path.unlink()
        
        # Also remove from frontier
        frontier = self.get_frontier_with_scores()
        frontier = [(n, s) for n, s in frontier if n != program_name]
        if frontier:
            self._frontier_path.write_text(json.dumps(frontier, indent=2))
        elif self._frontier_path.exists():
            self._frontier_path.unlink()
    
    def reset(self) -> None:
        """Reset the registry (delete all programs and frontier)"""
        # Delete all programs
        for program_file in self.programs_dir.glob("*.json"):
            program_file.unlink()
        
        # Delete frontier
        if self._frontier_path.exists():
            self._frontier_path.unlink()
        
        self._current_program = None
