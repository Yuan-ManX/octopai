#!/usr/bin/env python3
"""
Test import script to verify our modules work correctly.
"""
import sys
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("Testing imports...")

try:
    print("1. Testing evolution_core...")
    from evolution_core.feedback_descent import (
        SelectionStrategy,
        EvolutionMode,
        FeedbackDescent
    )
    print("   ✓ evolution_core imported successfully")

    print("2. Testing program_registry...")
    from program_registry.models import (
        ProgramStatus,
        SkillType,
        SkillMetadata,
        Skill,
        ProgramConfig,
        ProgramEntry,
        Experiment
    )
    print("   ✓ program_registry.models imported successfully")

    from program_registry.manager import ProgramRegistry
    print("   ✓ program_registry.manager imported successfully")

    print("3. Testing all together...")
    print("   ✓ All imports successful!")

except Exception as e:
    print(f"   ✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All imports test passed!")
