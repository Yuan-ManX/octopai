import os
import requests
from exo.utils.config import Config
from exo.utils.helpers import ensure_directory, fetch_url_content, extract_title, sanitize_filename, write_file
from exo.core.crawler import WebCrawler


class URLConverter:
    """URL to Markdown converter class"""
    
    def __init__(self):
        self.config = Config()
    
    def convert(self, url, output_dir=None, use_crawler: bool = False):
        """
        Convert URL to Markdown skill
        
        Args:
            url: The URL to convert
            output_dir: Optional output directory
            use_crawler: Whether to use the web crawler to download resources
            
        Returns:
            Path to the generated skill directory
        """
        # Validate configuration
        self.config.validate()
        
        # Fetch URL content
        html_content = fetch_url_content(url)
        
        # Extract title as skill name
        title = extract_title(html_content)
        skill_name = sanitize_filename(title)
        
        # Determine output directory
        if not output_dir:
            output_dir = os.path.join(self.config.SKILLS_DIR, skill_name)
        
        # Ensure output directories exist
        ensure_directory(output_dir)
        ensure_directory(os.path.join(output_dir, 'assets'))
        ensure_directory(os.path.join(output_dir, 'scripts'))
        ensure_directory(os.path.join(output_dir, 'references'))
        
        # Use crawler if requested
        if use_crawler:
            print(f"Using web crawler to download resources...")
            crawler_dir = os.path.join(output_dir, 'crawled')
            crawler = WebCrawler(crawler_dir)
            crawl_results = crawler.crawl(url)
            print(f"Crawled {crawl_results['total_files']} resources")
        
        # Call Cloudflare API to convert HTML to Markdown
        markdown_content = self._convert_html_to_markdown(html_content)
        
        # Generate SKILL.md file
        skill_metadata = self._generate_skill_metadata(title, url)
        skill_content = f"{skill_metadata}\n\n{markdown_content}"
        
        # Write files
        skill_file = os.path.join(output_dir, 'SKILL.md')
        write_file(skill_file, skill_content)
        
        # Write reference file
        reference_file = os.path.join(output_dir, 'references', 'source.md')
        write_file(reference_file, f"# Source\n\n- URL: {url}\n- Title: {title}")
        
        return output_dir
    
    def _convert_html_to_markdown(self, html_content):
        """Convert HTML to Markdown using Cloudflare API"""
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
            return result.get('result', {}).get('markdown', '')
        except Exception as e:
            raise Exception(f"Failed to convert HTML to Markdown: {str(e)}")
    
    def _generate_skill_metadata(self, title, url):
        """Generate skill metadata"""
        metadata = f"""
# {title}

## Metadata
- **name**: {title}
- **description**: Skill converted from {url}
- **author**: EXO
- **version**: 1.0.0
- **tags**:
  - web
  - markdown

## Instructions
This skill was automatically generated from a web URL. Use it to access information from the source.
"""
        return metadata.strip()
