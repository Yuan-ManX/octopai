"""
URL Converter - Enhanced URL Content Extractor for Skill Factory

This module provides intelligent URL content extraction and conversion
to structured Markdown format, optimized for Octopai's Skill Factory.
Enhanced to work seamlessly with the full-lifecycle skill creation framework.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from octopai.utils.config import Config
from octopai.utils.helpers import fetch_url_content, extract_title


@dataclass
class ExtractedURLContent:
    """Structured representation of extracted URL content"""
    url: str
    title: str
    raw_html: str
    markdown_content: str
    metadata: Dict[str, Any]


class URLConverter:
    """
    Enhanced URL to Markdown converter class for Skill Factory
    
    Focuses on content extraction rather than full skill packaging,
    leaving skill creation and optimization to SkillFactory.
    """
    
    def __init__(self):
        self.config = Config()
    
    def convert(self, url: str) -> str:
        """
        Convert URL to structured Markdown content (for Skill Factory)
        
        Args:
            url: The URL to convert
            
        Returns:
            Structured Markdown content ready for skill creation
        """
        extracted = self.extract(url)
        return self._format_for_skill_factory(extracted)
    
    def extract(self, url: str) -> ExtractedURLContent:
        """
        Extract comprehensive content from a URL
        
        Args:
            url: The URL to extract content from
            
        Returns:
            ExtractedURLContent with structured content and metadata
        """
        self.config.validate()
        
        html_content = fetch_url_content(url)
        title = extract_title(html_content)
        markdown_content = self._convert_html_to_markdown(html_content)
        
        metadata = {
            'url': url,
            'title': title,
            'extraction_timestamp': None,
            'content_type': 'webpage',
            'source': url
        }
        
        return ExtractedURLContent(
            url=url,
            title=title,
            raw_html=html_content,
            markdown_content=markdown_content,
            metadata=metadata
        )
    
    def _convert_html_to_markdown(self, html_content: str) -> str:
        """Convert HTML to Markdown with enhanced fallback mechanisms"""
        headers = {
            'Authorization': f'Bearer {self.config.CLOUDFLARE_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'html': html_content
        }
        
        try:
            response = requests.post(
                self.config.CLOUDFLARE_MARKDOWN_API,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            markdown = result.get('result', {}).get('markdown', '')
            if markdown:
                return markdown
        except Exception as e:
            print(f"Cloudflare API conversion failed: {e}")
        
        return self._fallback_html_to_markdown(html_content)
    
    def _fallback_html_to_markdown(self, html_content: str) -> str:
        """Fallback method to convert HTML to Markdown without external API"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for script in soup(["script", "style", "noscript"]):
                script.decompose()
            
            text = soup.get_text(separator='\n', strip=True)
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            
            return '\n\n'.join(lines)
        except ImportError:
            return html_content
    
    def _format_for_skill_factory(self, extracted: ExtractedURLContent) -> str:
        """Format extracted content for use in Skill Factory"""
        parts = []
        
        parts.append(f"# Source: {extracted.title}")
        parts.append(f"**URL**: {extracted.url}")
        parts.append("")
        
        parts.append("## Extracted Content")
        parts.append(extracted.markdown_content)
        
        parts.append("")
        parts.append("---")
        parts.append("## Source Metadata")
        parts.append(f"- **Source URL**: {extracted.url}")
        parts.append(f"- **Title**: {extracted.title}")
        parts.append("- **Extracted by**: Octopai URL Converter")
        
        return '\n'.join(parts)


def convert_url_to_content(url: str) -> str:
    """
    Convenience function to convert URL to content
    
    Args:
        url: URL to convert
        
    Returns:
        Structured content string
    """
    converter = URLConverter()
    return converter.convert(url)


def extract_url_content(url: str) -> ExtractedURLContent:
    """
    Convenience function to extract comprehensive URL content
    
    Args:
        url: URL to extract from
        
    Returns:
        ExtractedURLContent object
    """
    converter = URLConverter()
    return converter.extract(url)
