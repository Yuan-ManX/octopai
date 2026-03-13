"""
Tests for Evolution Engine module

Tests the skill evolution capabilities.
"""

import os
import tempfile
import pytest
from exo.core.evolution_engine import (
    EvolutionTrace,
    SkillCandidate,
    EvolutionEngine
)


class TestEvolutionTrace:
    """Tests for EvolutionTrace class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        trace = EvolutionTrace()
        
        assert trace.success is False
        assert trace.error_messages == []
        assert trace.reasoning_logs == []
        assert trace.performance_metrics == {}
        assert trace.other_info == {}
    
    def test_add_error(self):
        """Test adding error messages"""
        trace = EvolutionTrace()
        
        trace.add_error("Test error 1")
        trace.add_error("Test error 2")
        
        assert len(trace.error_messages) == 2
        assert "Test error 1" in trace.error_messages
        assert "Test error 2" in trace.error_messages
    
    def test_add_reasoning(self):
        """Test adding reasoning logs"""
        trace = EvolutionTrace()
        
        trace.add_reasoning("Step 1 complete")
        trace.add_reasoning("Step 2 complete")
        
        assert len(trace.reasoning_logs) == 2
        assert "Step 1 complete" in trace.reasoning_logs
    
    def test_add_metric(self):
        """Test adding performance metrics"""
        trace = EvolutionTrace()
        
        trace.add_metric("accuracy", 0.85)
        trace.add_metric("speed", 1.2)
        
        assert trace.performance_metrics["accuracy"] == 0.85
        assert trace.performance_metrics["speed"] == 1.2
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        trace = EvolutionTrace()
        trace.success = True
        trace.add_error("Test error")
        trace.add_reasoning("Test reasoning")
        trace.add_metric("test", 1.0)
        
        trace_dict = trace.to_dict()
        
        assert trace_dict["success"] is True
        assert "Test error" in trace_dict["error_messages"]
        assert "Test reasoning" in trace_dict["reasoning_logs"]
        assert trace_dict["performance_metrics"]["test"] == 1.0


class TestSkillCandidate:
    """Tests for SkillCandidate class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        candidate = SkillCandidate("test content", version=1)
        
        assert candidate.content == "test content"
        assert candidate.version == 1
        assert candidate.fitness == 0.0
        assert candidate.trace is None
        assert candidate.ancestors == []
    
    def test_to_dict(self):
        """Test conversion to dictionary"""
        candidate = SkillCandidate("test content", version=2)
        candidate.fitness = 0.9
        candidate.ancestors = ["v1"]
        
        candidate_dict = candidate.to_dict()
        
        assert candidate_dict["content"] == "test content"
        assert candidate_dict["version"] == 2
        assert candidate_dict["fitness"] == 0.9
        assert candidate_dict["ancestors"] == ["v1"]


class TestEvolutionEngine:
    """Tests for EvolutionEngine class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        engine = EvolutionEngine()
        
        assert engine.pareto_frontier == []
        assert engine.max_iterations == 10
        assert engine.current_iteration == 0
    
    def test_executor(self):
        """Test the executor stage"""
        engine = EvolutionEngine()
        candidate = SkillCandidate("test content")
        
        trace = engine.executor(candidate)
        
        assert isinstance(trace, EvolutionTrace)
        # The executor sets success to True in the current implementation
    
    def test_evaluate_fitness_no_trace(self):
        """Test fitness evaluation without trace"""
        engine = EvolutionEngine()
        candidate = SkillCandidate("test content")
        
        fitness = engine.evaluate_fitness(candidate)
        
        assert fitness == 0.0
    
    def test_evaluate_fitness_with_trace(self):
        """Test fitness evaluation with trace"""
        engine = EvolutionEngine()
        candidate = SkillCandidate("test content")
        
        trace = EvolutionTrace()
        trace.add_metric("accuracy", 0.8)
        trace.add_metric("completeness", 0.9)
        candidate.trace = trace
        
        fitness = engine.evaluate_fitness(candidate)
        
        # Should be average of metrics: (0.8 + 0.9) / 2 = 0.85
        assert fitness == pytest.approx(0.85)
    
    def test_reflector(self):
        """Test the reflector stage (with mocking)"""
        engine = EvolutionEngine()
        traces = [EvolutionTrace()]
        
        # The reflector requires API key, but we can still call it
        # It should handle the missing API key gracefully
        diagnosis = engine.reflector(traces)
        
        assert isinstance(diagnosis, str)
    
    def test_curator(self):
        """Test the curator stage (with mocking)"""
        engine = EvolutionEngine()
        candidate = SkillCandidate("test content", version=1)
        
        # The curator requires API key, but we can still call it
        # It should handle the missing API key gracefully
        result = engine.curator("Test diagnosis", candidate)
        
        assert isinstance(result, SkillCandidate)


class TestEvolutionIntegration:
    """Integration tests for evolution process"""
    
    def test_evolution_engine_smoke(self):
        """Smoke test for evolution engine"""
        engine = EvolutionEngine()
        
        # Just test that we can create and use the engine
        # without exceptions
        candidate = SkillCandidate("def test(): pass")
        trace = engine.executor(candidate)
        
        assert trace is not None
    
    def test_pareto_frontier_management(self):
        """Test that pareto frontier is initialized"""
        engine = EvolutionEngine()
        
        assert isinstance(engine.pareto_frontier, list)
        assert len(engine.pareto_frontier) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
