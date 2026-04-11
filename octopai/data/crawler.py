"""
Web Crawler for Octopai

This module provides web crawling capabilities to fetch and save content from URLs as skill resources.
"""

import os
import re
import time
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from octopai.utils.helpers import ensure_directory, write_file, fetch_url_content


class WebResource:
    """
    Represents a web resource (HTML, image, CSS, JS, etc.)
    """
    
    def __init__(self, url: str, content: bytes, content_type: str):
        self.url = url
        self.content = content
        self.content_type = content_type
        self.filename: Optional[str] = None
    
    def get_extension(self) -> str:
        """Get appropriate file extension based on content type"""
        if 'html' in self.content_type:
            return '.html'
        elif 'css' in self.content_type:
            return '.css'
        elif 'javascript' in self.content_type or 'js' in self.content_type:
            return '.js'
        elif 'image/png' in self.content_type:
            return '.png'
        elif 'image/jpeg' in self.content_type or 'image/jpg' in self.content_type:
            return '.jpg'
        elif 'image/gif' in self.content_type:
            return '.gif'
        elif 'image/svg' in self.content_type:
            return '.svg'
        elif 'text/plain' in self.content_type:
            return '.txt'
        else:
            return '.bin'


class WebCrawler:
    """
    Web crawler for fetching and saving web content
    
    Features:
    - HTML content extraction
    - Image downloading
    - CSS and JS file saving
    - Resource link rewriting
    - Rate limiting and polite crawling
    """
    
    def __init__(self, output_dir: str):
        """
        Initialize the crawler
        
        Args:
            output_dir: Directory to save crawled content
        """
        self.output_dir = output_dir
        self.assets_dir = os.path.join(output_dir, 'assets')
        self.html_dir = os.path.join(output_dir, 'html')
        self.css_dir = os.path.join(output_dir, 'css')
        self.js_dir = os.path.join(output_dir, 'js')
        self.images_dir = os.path.join(output_dir, 'images')
        
        # Ensure all directories exist
        ensure_directory(self.assets_dir)
        ensure_directory(self.html_dir)
        ensure_directory(self.css_dir)
        ensure_directory(self.js_dir)
        ensure_directory(self.images_dir)
        
        # Track visited URLs to avoid duplicates
        self.visited_urls: set = set()
        
        # Rate limiting
        self.request_delay: float = 1.0
    
    def sanitize_filename(self, url: str) -> str:
        """
        Create a safe filename from a URL
        
        Args:
            url: The URL to sanitize
            
        Returns:
            Safe filename
        """
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        if not path:
            path = 'index'
        
        # Replace unsafe characters
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', path)
        
        # Truncate if too long
        if len(safe_name) > 100:
            safe_name = safe_name[:100]
        
        return safe_name
    
    def download_resource(self, url: str) -> Optional[WebResource]:
        """
        Download a single web resource
        
        Args:
            url: The URL to download
            
        Returns:
            WebResource object or None if failed
        """
        if url in self.visited_urls:
            return None
        
        try:
            # Respect rate limiting
            time.sleep(self.request_delay)
            
            response = requests.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            content = response.content
            content_type = response.headers.get('content-type', '')
            
            resource = WebResource(url, content, content_type)
            self.visited_urls.add(url)
            
            return resource
            
        except Exception as e:
            print(f"Failed to download {url}: {str(e)}")
            return None
    
    def save_resource(self, resource: WebResource, subdir: Optional[str] = None) -> str:
        """
        Save a web resource to disk
        
        Args:
            resource: The resource to save
            subdir: Optional subdirectory
            
        Returns:
            Path to the saved file
        """
        # Determine target directory
        if subdir:
            target_dir = os.path.join(self.assets_dir, subdir)
        elif 'html' in resource.content_type:
            target_dir = self.html_dir
        elif 'css' in resource.content_type:
            target_dir = self.css_dir
        elif 'javascript' in resource.content_type or 'js' in resource.content_type:
            target_dir = self.js_dir
        elif 'image' in resource.content_type:
            target_dir = self.images_dir
        else:
            target_dir = self.assets_dir
        
        ensure_directory(target_dir)
        
        # Generate filename
        base_name = self.sanitize_filename(resource.url)
        extension = resource.get_extension()
        filename = f"{base_name}{extension}"
        
        # Ensure unique filename
        counter = 1
        filepath = os.path.join(target_dir, filename)
        while os.path.exists(filepath):
            filepath = os.path.join(target_dir, f"{base_name}_{counter}{extension}")
            counter += 1
        
        # Save binary content
        with open(filepath, 'wb') as f:
            f.write(resource.content)
        
        resource.filename = os.path.relpath(filepath, self.output_dir)
        return filepath
    
    def extract_links(self, html: str, base_url: str) -> List[str]:
        """
        Extract all resource links from HTML
        
        Args:
            html: HTML content
            base_url: Base URL for resolving relative links
            
        Returns:
            List of absolute URLs
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        # Extract image sources
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                links.append(urljoin(base_url, src))
        
        # Extract CSS links
        for css in soup.find_all('link', rel='stylesheet'):
            href = css.get('href')
            if href:
                links.append(urljoin(base_url, href))
        
        # Extract JS links
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                links.append(urljoin(base_url, src))
        
        return links
    
    def crawl(self, url: str, follow_links: bool = False, max_depth: int = 1) -> Dict[str, Any]:
        """
        Crawl a URL and save all resources
        
        Args:
            url: The starting URL
            follow_links: Whether to follow links to other pages
            max_depth: Maximum crawl depth
            
        Returns:
            Dictionary with crawl results
        """
        print(f"Starting crawl of: {url}")
        
        results = {
            'url': url,
            'html_files': [],
            'css_files': [],
            'js_files': [],
            'image_files': [],
            'other_files': [],
            'total_files': 0
        }
        
        # Download main HTML
        html_resource = self.download_resource(url)
        if not html_resource:
            return results
        
        # Save HTML file
        html_path = self.save_resource(html_resource)
        results['html_files'].append(html_path)
        
        # Extract and save linked resources
        html_content = html_resource.content.decode('utf-8', errors='ignore')
        links = self.extract_links(html_content, url)
        
        print(f"Found {len(links)} resource links")
        
        for link in links:
            resource = self.download_resource(link)
            if resource:
                resource_path = self.save_resource(resource)
                
                if 'html' in resource.content_type:
                    results['html_files'].append(resource_path)
                elif 'css' in resource.content_type:
                    results['css_files'].append(resource_path)
                elif 'javascript' in resource.content_type or 'js' in resource.content_type:
                    results['js_files'].append(resource_path)
                elif 'image' in resource.content_type:
                    results['image_files'].append(resource_path)
                else:
                    results['other_files'].append(resource_path)
        
        results['total_files'] = sum([
            len(results['html_files']),
            len(results['css_files']),
            len(results['js_files']),
            len(results['image_files']),
            len(results['other_files'])
        ])
        
        print(f"Crawl complete. Saved {results['total_files']} files.")
        
        # Save crawl metadata
        metadata_path = os.path.join(self.output_dir, 'crawl_metadata.json')
        import json
        write_file(metadata_path, json.dumps(results, indent=2))
        
        return results


def crawl_url(url: str, output_dir: str, follow_links: bool = False) -> Dict[str, Any]:
    """
    Convenience function to crawl a URL
    
    Args:
        url: The URL to crawl
        output_dir: Output directory
        follow_links: Whether to follow links
        
    Returns:
        Crawl results
    """
    crawler = WebCrawler(output_dir)
    return crawler.crawl(url, follow_links)
