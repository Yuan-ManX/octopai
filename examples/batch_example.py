#!/usr/bin/env python3
"""
Octopai batch processing example
"""

import os
from octopai.core.converter import URLConverter
from octopai.core.creator import SkillCreator


def main():
    """Example main function"""
    # 1. Initialize modules
    converter = URLConverter()
    creator = SkillCreator()
    
    # 2. Define list of URLs to process
    urls = [
        "https://example.com",
        "https://github.com",
        "https://openrouter.ai"
    ]
    
    # 3. Batch processing
    output_dir = "./batch_skills"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, url in enumerate(urls):
        try:
            print(f"Processing URL {i+1}: {url}")
            skill_dir = converter.convert(url, os.path.join(output_dir, f"skill_{i}"))
            creator.create(skill_dir)
            print(f"Processing complete: {skill_dir}")
        except Exception as e:
            print(f"Processing failed: {str(e)}")
    
    print("Batch processing complete!")


if __name__ == "__main__":
    main()
