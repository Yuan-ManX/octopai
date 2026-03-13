"""
EXO usage example
"""

from exo.core.converter import URLConverter
from exo.core.creator import SkillCreator
from exo.core.evolver import SkillEvolver


def main():
    """Example main function"""
    # 1. Initialize modules
    converter = URLConverter()
    creator = SkillCreator()
    evolver = SkillEvolver()
    
    # 2. Convert URL to skill
    url = "https://example.com"
    print(f"Converting URL: {url}")
    skill_dir = converter.convert(url)
    print(f"Conversion complete, skill directory: {skill_dir}")
    
    # 3. Create standard skill
    print("Creating standard skill format...")
    creator.create(skill_dir)
    print("Skill creation complete")
    
    # 4. Evolve skill
    print("Evolving skill content...")
    evolver.evolve(skill_dir)
    print("Skill evolution complete")
    
    print("Example execution complete!")


if __name__ == "__main__":
    main()
