"""
Octopai Data Module - Data Acquisition and Processing System
Web crawling, resource parsing, URL conversion, and data extraction
"""

from .crawler import WebCrawler
from .parser import ResourceParser, ParsedResource, ResourceType, parse_resource, parse_to_skill_resource
from .converter import URLConverter

__all__ = [
    'WebCrawler',
    'ResourceParser', 'ParsedResource', 'ResourceType', 'parse_resource', 'parse_to_skill_resource',
    'URLConverter'
]
