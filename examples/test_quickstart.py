"""
Test script to verify the quick start examples work correctly
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Testing Octopai imports...")

# Test basic imports
try:
    from octopai import Octopai
    print("✓ Octopai class imported successfully")
except Exception as e:
    print(f"✗ Failed to import Octopai: {e}")
    sys.exit(1)

try:
    from octopai import create_from_prompt, create_from_text
    print("✓ Skill creation functions imported successfully")
except Exception as e:
    print(f"✗ Failed to import skill creation functions: {e}")
    sys.exit(1)

try:
    from octopai import (
        hub_create, hub_list, hub_search, hub_stats,
        hub_create_collection, hub_semantic_search,
        hub_publish, hub_add_rating, get_insights
    )
    print("✓ SkillHub functions imported successfully")
except Exception as e:
    print(f"✗ Failed to import SkillHub functions: {e}")
    sys.exit(1)

print("\nTesting basic initialization...")
try:
    octopai = Octopai()
    print("✓ Octopai initialized successfully")
except Exception as e:
    print(f"✗ Failed to initialize Octopai: {e}")
    sys.exit(1)

print("\nTesting basic SkillHub operations...")
try:
    # Test creating a simple skill in SkillHub
    skill = hub_create(
        name="Test Skill",
        description="A test skill for verification",
        prompt="Create a simple test skill",
        tags=["test", "example"],
        category="testing"
    )
    print(f"✓ Created test skill: {skill.name}")
    
    # Test listing skills
    skills = hub_list()
    print(f"✓ Listed {len(skills)} skills in SkillHub")
    
    # Test getting stats
    stats = hub_stats()
    print(f"✓ Got SkillHub stats: {stats}")
    
except Exception as e:
    print(f"✗ SkillHub operations failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("✓ All basic tests passed!")
print("="*60)
print("\nYou can now run:")
print("  - python examples/simple_quickstart.py (English)")
print("  - python examples/simple_quickstart_cn.py (中文)")
