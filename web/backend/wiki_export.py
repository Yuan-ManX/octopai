"""
Export System for AI Wiki - Multi-Format Data Export

Supported Export Formats:
1. Markdown (.md) - Human-readable wiki format with full formatting
2. PDF (.pdf) - Professional document format for sharing/printing
3. JSON (.json) - Machine-readable structured data for integration
4. CSV (.csv) - Spreadsheet-compatible tabular data
5. HTML (.html) - Web-ready interactive documentation

Export Scenarios:
- Single Wiki Page: Individual page with metadata
- Multiple Pages: Batch export of selected pages
- Full Knowledge Base: Complete wiki dump
- Knowledge Graph: Graph structure in various formats
- Trace Timeline: Operation history and analytics
- Cost Reports: Token usage and budget reports
- Lint Reports: Quality assurance results

Features:
- Asynchronous job processing for large exports
- Progress tracking and status updates
- File size optimization and compression
- Custom templates for branded exports
- Batch operations support
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import uuid
import io


class ExportFormat(Enum):
    """Supported export formats"""
    MARKDOWN = "markdown"
    PDF = "pdf"
    JSON = "json"
    CSV = "csv"
    HTML = "html"


class ExportType(Enum):
    """Export type/scenario enumeration"""
    WIKI_PAGE = "wiki_page"
    WIKI_PAGES_BATCH = "wiki_pages_batch"
    FULL_KNOWLEDGE_BASE = "full_knowledge_base"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    TRACE_TIMELINE = "trace_timeline"
    COST_REPORT = "cost_report"
    LINT_REPORT = "lint_report"
    ACTIVITY_LOG = "activity_log"


@dataclass
class ExportJob:
    """Export job tracking object"""
    job_id: str
    user_id: str
    export_format: ExportFormat
    export_type: ExportType
    entity_ids: List[str] = field(default_factory=list)
    options: Dict = field(default_factory=dict)
    
    # Status tracking
    status: str = "pending"  # pending, processing, completed, failed
    progress: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Results
    file_path: Optional[str] = None
    file_size: int = 0
    record_count: int = 0
    
    # Error handling
    error_message: Optional[str] = None


@dataclass
class ExportResult:
    """Final result of an export operation"""
    success: bool
    job_id: str
    file_path: str
    file_size: int
    format: str
    record_count: int
    duration_seconds: float
    download_url: Optional[str] = None
    error_message: Optional[str] = None


class MarkdownExporter:
    """Export handler for Markdown format"""
    
    @staticmethod
    def export_wiki_page(page_data: Dict) -> str:
        """Export single wiki page to Markdown"""
        lines = []
        
        # YAML frontmatter
        lines.append('---')
        frontmatter = page_data.get('frontmatter', {})
        for key, value in frontmatter.items():
            if isinstance(value, (list, dict)):
                lines.append(f'{key}: {json.dumps(value)}')
            else:
                lines.append(f'{key}: {value}')
        lines.append('---')
        lines.append('')
        
        # Title and content
        title = page_data.get('title', 'Untitled')
        lines.append(f'# {title}')
        lines.append('')
        
        content = page_data.get('content', '')
        lines.append(content)
        
        # Metadata footer
        lines.append('')
        lines.append('---')
        lines.append(f'*Page ID: {page_data.get("id", "unknown")}*')
        lines.append(f'*Type: {page_data.get("page_type", "unknown")}*')
        lines.append(f'*Quality Score: {page_data.get("quality_score", "N/A")}*')
        if page_data.get('updated_at'):
            lines.append(f'*Last Updated: {page_data["updated_at"]}*')
        
        return '\n'.join(lines)
    
    @staticmethod
    def export_multiple_pages(pages: List[Dict], include_toc: bool = True) -> str:
        """Export multiple pages as a single Markdown document"""
        sections = []
        
        # Table of contents
        if include_toc:
            toc_lines = ['# Table of Contents\n']
            for i, page in enumerate(pages, 1):
                title = page.get('title', f'Page {i}')
                page_type = page.get('page_type', '')
                toc_lines.append(f'{i}. [{title}](#{title.lower().replace(" ", "-")}) ({page_type})')
            sections.append('\n'.join(toc_lines))
            sections.append('\n---\n')
        
        # Each page content
        for page in pages:
            sections.append(MarkdownExporter.export_wiki_page(page))
            sections.append('\n\n---\n\n')  # Separator
        
        return '\n'.join(sections)
    
    @staticmethod
    def export_knowledge_graph(graph_data: Dict) -> str:
        """Export knowledge graph structure to Markdown"""
        lines = []
        lines.append('# Knowledge Graph Export')
        lines.append('')
        lines.append(f'*Generated: {datetime.now().isoformat()}*')
        lines.append('')
        
        # Nodes section
        nodes = graph_data.get('nodes', [])
        lines.append(f'## Nodes ({len(nodes)})\n')
        for node in nodes:
            label = node.get('label', 'Unknown')
            group = node.get('group_type', 'concept')
            connections = node.get('connections', 0)
            lines.append(f'- **{label}** ({group}) - {connections} connections')
        lines.append('')
        
        # Edges section
        edges = graph_data.get('edges', [])
        lines.append(f'\n## Edges ({len(edges)})\n')
        for edge in edges:
            source = edge.get('source_node_id', '?')
            target = edge.get('target_node_id', '?')
            weight = edge.get('weight', 0)
            edge_type = edge.get('edge_type', 'related')
            lines.append(f'- {source} --[{edge_type}: {weight:.2f}]--> {target}')
        
        return '\n'.join(lines)


class JSONExporter:
    """Export handler for JSON format"""
    
    @staticmethod
    def export_wiki_page(page_data: Dict) -> str:
        """Export single wiki page to JSON"""
        export_obj = {
            "export_format": "json",
            "export_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "page": {
                **page_data,
                "frontmatter": json.loads(page_data.get('frontmatter', '{}'))
                if isinstance(page_data.get('frontmatter'), str)
                else page_data.get('frontmatter', {})
            }
        }
        return json.dumps(export_obj, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_multiple_pages(pages: List[Dict]) -> str:
        """Export multiple pages to JSON array"""
        export_obj = {
            "export_format": "json",
            "export_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "total_pages": len(pages),
            "pages": [
                {
                    **page,
                    "frontmatter": json.loads(page.get('frontmatter', '{}'))
                    if isinstance(page.get('frontmatter'), str)
                    else page.get('frontmatter', {})
                }
                for page in pages
            ]
        }
        return json.dumps(export_obj, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_trace_timeline(timeline_data: Dict) -> str:
        """Export trace timeline to JSON"""
        export_obj = {
            "export_format": "json",
            "export_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            **timeline_data
        }
        return json.dumps(export_obj, indent=2, ensure_ascii=False)
    
    @staticmethod
    def export_cost_analytics(cost_data: Dict) -> str:
        """Export cost analytics to JSON"""
        export_obj = {
            "export_format": "json",
            "export_version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "report_type": "cost_analytics",
            **cost_data
        }
        return json.dumps(export_obj, indent=2, ensure_ascii=False)


class CSVExporter:
    """Export handler for CSV/Spreadsheet format"""
    
    @staticmethod
    def export_pages_table(pages: List[Dict]) -> str:
        """Export wiki pages summary table to CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header row
        writer.writerow([
            'ID', 'Title', 'Type', 'Quality Score', 'Version',
            'Created At', 'Updated At', 'Status'
        ])
        
        # Data rows
        for page in pages:
            writer.writerow([
                page.get('id', ''),
                page.get('title', ''),
                page.get('page_type', ''),
                page.get('quality_score', ''),
                page.get('version', ''),
                page.get('created_at', ''),
                page.get('updated_at', ''),
                page.get('status', '')
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_timeline_table(events: List[Dict]) -> str:
        """Export timeline events to CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'Timestamp', 'Operation', 'Source', 'Details',
            'Duration', 'Tokens', 'Cost', 'Span ID'
        ])
        
        for event in events:
            writer.writerow([
                event.get('timestamp', ''),
                event.get('operation', ''),
                event.get('source', ''),
                event.get('details', '')[:100],
                event.get('duration', ''),
                event.get('tokens', ''),
                event.get('cost', ''),
                event.get('span_id', '')
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_cost_records(records: List[Dict]) -> str:
        """Export cost records to CSV"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        writer.writerow([
            'Timestamp', 'Operation', 'Tokens', 'Cost (USD)',
            'Layer', 'User ID'
        ])
        
        for record in records:
            writer.writerow([
                record.get('timestamp', ''),
                record.get('operation', ''),
                record.get('tokens', ''),
                record.get('cost', ''),
                record.get('layer', ''),
                record.get('user_id', '')
            ])
        
        return output.getvalue()


class HTMLExporter:
    """Export handler for HTML format (web-ready)"""
    
    @staticmethod
    def export_wiki_page(page_data: Dict) -> str:
        """Export single wiki page to styled HTML"""
        title = page_data.get('title', 'Untitled')
        content = page_data.get('content', '')
        page_type = page_data.get('page_type', 'unknown')
        quality = page_data.get('quality_score', 0)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title} - AI Wiki</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               max-width: 900px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
        h1 {{ color: #1a1a1a; border-bottom: 3px solid #f59e0b; padding-bottom: 10px; }}
        .metadata {{ background: #f9fafb; border-left: 4px solid #3b82f6; 
                   padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .badge {{ display: inline-block; padding: 4px 12px; border-radius: 12px; 
                 font-size: 0.85em; font-weight: 600; margin-right: 8px; }}
        .badge-entity {{ background: #dbeafe; color: #1e40af; }}
        .badge-concept {{ background: #fce7f3; color: #9d174d; }}
        .quality {{ font-size: 1.2em; font-weight: bold; color: {self._quality_color(quality)}; }}
        pre {{ background: #1e293b; color: #e2e8f0; padding: 16px; border-radius: 8px; overflow-x: auto; }}
        code {{ background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="metadata">
        <span class="badge badge-{page_type}">{page_type}</span>
        <span class="quality">Quality: {quality}/100</span>
        <p><strong>ID:</strong> {page_data.get('id', 'N/A')}</p>
        <p><strong>Last Updated:</strong> {page_data.get('updated_at', 'N/A')}</p>
    </div>
    <div class="content">
        {HTMLExporter._markdown_to_html(content)}
    </div>
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; 
            color: #6b7280; font-size: 0.9em;">
        <p>Exported from AI Wiki on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
</body>
</html>'''
        return html
    
    @staticmethod
    def _quality_color(score: int) -> str:
        """Get color based on quality score"""
        if score >= 90: return '#059669'
        elif score >= 70: return '#d97706'
        else: return '#dc2626'
    
    @staticmethod
    def _markdown_to_html(markdown_text: str) -> str:
        """
        Simple markdown to HTML converter
        In production, use a proper library like markdown or mistune
        """
        # Basic conversion rules
        html = markdown_text
        
        # Headers
        import re
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        
        # Code blocks
        html = re.sub(r'```(\w*)\n(.+?)```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
        
        # Lists
        html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html)
        
        # Links
        html = re.sub(r'\[\[(.+?)\]\]', r'<a href="#\1">\1</a>', html)
        
        # Paragraphs
        html = re.sub(r'\n\n+', '</p><p>', html)
        html = f'<p>{html}</p>'
        
        # Clean up empty paragraphs
        html = re.sub(r'<p>\s*</p>', '', html)
        
        return html


class PDFExporter:
    """Export handler for PDF format (requires additional dependencies)"""
    
    @staticmethod
    def export_to_pdf(html_content: str, output_path: str) -> bool:
        """
        Convert HTML content to PDF using wkhtmltopdf or similar
        
        Note: Requires wkhtmltopdf installed or pdfkit Python package
        """
        try:
            # Try using pdfkit if available
            import pdfkit
            
            config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
            pdfkit.from_string(html_content, output_path, configuration=config)
            return True
            
        except ImportError:
            print("[Export] PDF generation requires 'pdfkit' package")
            return False
        except Exception as e:
            print(f"[Export] PDF generation error: {e}")
            return False


class ExportManager:
    """
    Central export manager coordinating all export operations
    
    Features:
    - Format detection and routing
    - Job queue management
    - Progress tracking
    - Async processing support
    - File management
    """
    
    def __init__(self, export_dir: str = "exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(exist_ok=True)
        
        self.jobs: Dict[str, ExportJob] = {}
        
        # Format handlers mapping
        self.format_handlers = {
            ExportFormat.MARKDOWN: MarkdownExporter,
            ExportFormat.JSON: JSONExporter,
            ExportFormat.CSV: CSVExporter,
            ExportFormat.HTML: HTMLExporter,
            ExportFormat.PDF: PDFExporter
        }
    
    def create_export_job(
        self,
        user_id: str,
        export_format: ExportFormat,
        export_type: ExportType,
        entity_ids: List[str] = None,
        options: Dict = None
    ) -> str:
        """
        Create a new export job
        
        Returns:
            Job ID for tracking
        """
        job_id = f"export_{uuid.uuid4().hex[:8]}"
        
        job = ExportJob(
            job_id=job_id,
            user_id=user_id,
            export_format=export_format,
            export_type=export_type,
            entity_ids=entity_ids or [],
            options=options or {}
        )
        
        self.jobs[job_id] = job
        return job_id
    
    async def execute_export_job(self, job_id: str, data_provider) -> ExportResult:
        """
        Execute an export job asynchronously
        
        Args:
            job_id: Job identifier
            data_provider: Callable that returns the data to export
            
        Returns:
            ExportResult with outcome details
        """
        start_time = datetime.now()
        
        if job_id not in self.jobs:
            return ExportResult(
                success=False,
                job_id=job_id,
                file_path='',
                file_size=0,
                format='',
                record_count=0,
                duration_seconds=0,
                error_message="Job not found"
            )
        
        job = self.jobs[job_id]
        job.status = "processing"
        job.started_at = datetime.now()
        
        try:
            # Get data from provider
            data = await data_provider(job.entity_ids, job.options)
            
            # Generate content based on format
            content = self._generate_content(job.export_format, job.export_type, data)
            
            # Determine filename and path
            filename = self._generate_filename(job)
            filepath = self.export_dir / filename
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Update job status
            job.status = "completed"
            job.completed_at = datetime.now()
            job.file_path = str(filepath)
            job.file_size = os.path.getsize(filepath)
            job.progress = 100
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return ExportResult(
                success=True,
                job_id=job_id,
                file_path=str(filepath),
                file_size=job.file_size,
                format=job.export_format.value,
                record_count=len(data) if isinstance(data, list) else 1,
                duration_seconds=duration,
                download_url=f"/api/export/download/{filename}"
            )
            
        except Exception as e:
            job.status = "failed"
            job.error_message = str(e)
            
            return ExportResult(
                success=False,
                job_id=job_id,
                file_path='',
                file_size=0,
                format=job.export_format.value,
                record_count=0,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                error_message=str(e)
            )
    
    def _generate_content(self, fmt: ExportFormat, export_type: ExportType, 
                         data: Any) -> str:
        """Generate export content based on format and type"""
        handler = self.format_handlers.get(fmt)
        
        if fmt == ExportFormat.MARKDOWN:
            if export_type == ExportType.WIKI_PAGE:
                return handler.export_wiki_page(data)
            elif export_type == ExportType.WIKI_PAGES_BATCH or export_type == ExportType.FULL_KNOWLEDGE_BASE:
                return handler.export_multiple_pages(data)
            elif export_type == ExportType.KNOWLEDGE_GRAPH:
                return handler.export_knowledge_graph(data)
                
        elif fmt == ExportFormat.JSON:
            if export_type == ExportType.WIKI_PAGE:
                return handler.export_wiki_page(data)
            elif export_type in [ExportType.WIKI_PAGES_BATCH, ExportType.FULL_KNOWLEDGE_BASE]:
                return handler.export_multiple_pages(data)
            elif export_type == ExportType.TRACE_TIMELINE:
                return handler.export_trace_timeline(data)
            elif export_type == ExportType.COST_REPORT:
                return handler.export_cost_analytics(data)
                
        elif fmt == ExportFormat.CSV:
            if export_type in [ExportType.WIKI_PAGE, ExportType.WIKI_PAGES_BATCH]:
                return handler.export_pages_table(data if isinstance(data, list) else [data])
            elif export_type == ExportType.TRACE_TIMELINE:
                events = data.get('events', []) if isinstance(data, dict) else data
                return handler.export_timeline_table(events)
            elif export_type == ExportType.COST_REPORT:
                records = []  # Would need to extract from cost_data
                return handler.export_cost_records(records)
                
        elif fmt == ExportFormat.HTML:
            if export_type == ExportType.WIKI_PAGE:
                return handler.export_wiki_page(data)
        
        raise ValueError(f"Unsupported combination: {fmt.value} + {export_type.value}")
    
    def _generate_filename(self, job: ExportJob) -> str:
        """Generate unique filename for export"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        type_name = job.export_type.value
        format_ext = {
            ExportFormat.MARKDOWN: '.md',
            ExportFormat.PDF: '.pdf',
            ExportFormat.JSON: '.json',
            ExportFormat.CSV: '.csv',
            ExportFormat.HTML: '.html'
        }.get(job.export_format, '.txt')
        
        return f"{type_name}_{timestamp}_{job.job_id[:8]}{format_ext}"
    
    def get_job_status(self, job_id: str) -> Optional[Dict]:
        """Get current status of an export job"""
        if job_id not in self.jobs:
            return None
        
        job = self.jobs[job_id]
        return {
            "job_id": job.job_id,
            "status": job.status,
            "progress": job.progress,
            "format": job.export_format.value,
            "type": job.export_type.value,
            "file_path": job.file_path,
            "file_size": job.file_size,
            "record_count": job.record_count,
            "created_at": job.created_at.isoformat() if job.created_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "error_message": job.error_message
        }
    
    def cleanup_old_exports(self, max_age_hours: int = 24) -> int:
        """Remove export files older than specified age"""
        count = 0
        cutoff = datetime.now() - timedelta(hours=max_age_hours)
        
        for filepath in self.export_dir.iterdir():
            if filepath.is_file():
                file_mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                if file_mtime < cutoff:
                    filepath.unlink()
                    count += 1
        
        return count


# Global instance
export_manager_instance: Optional[ExportManager] = None


def get_export_manager() -> ExportManager:
    """Get or create global export manager instance"""
    global export_manager_instance
    if export_manager_instance is None:
        export_manager_instance = ExportManager()
    return export_manager_instance
