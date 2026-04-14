"""
Version Control System for AI Wiki Pages - Complete History and Diff Comparison

Features:
- Full version history for every wiki page
- Automatic snapshot on each save/edit
- Diff generation between any two versions
- Version restoration (rollback to previous version)
- Change tracking with author attribution
- Branching support (experimental features)
- Merge conflict detection
- Visual diff representation (HTML-formatted)

Data Structures:
- PageVersion: Individual snapshot of a page at a point in time
- DiffResult: Structured comparison between two versions
- ChangeSet: Collection of changes in a single edit operation

Diff Algorithms:
- Line-by-line comparison for text content
- Word-level changes detection
- Structural diff for frontmatter metadata
- Semantic change categorization (addition, deletion, modification)
"""

import difflib
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re


class ChangeType(Enum):
    """Type of change between versions"""
    ADDED = "added"
    DELETED = "deleted"
    MODIFIED = "modified"
    UNCHANGED = "unchanged"
    MOVED = "moved"


@dataclass
class DiffLine:
    """Single line in a diff output"""
    line_number: int
    content: str
    change_type: ChangeType
    old_line_number: Optional[int] = None  # For modified/moved lines


@dataclass
class DiffResult:
    """Complete diff result between two versions"""
    version_a: int
    version_b: int
    has_changes: bool
    lines_added: int = 0
    lines_deleted: int = 0
    lines_modified: int = 0
    lines_unchanged: int = 0
    diff_lines: List[DiffLine] = field(default_factory=list)
    summary: str = ""
    similarity_score: float = 1.0


@dataclass
class PageVersion:
    """Snapshot of a wiki page at a specific version"""
    version_id: str
    page_id: str
    version_number: int
    content: str
    frontmatter: Dict[str, Any]
    author_id: str
    author_username: str
    change_summary: str
    created_at: datetime
    diff_from_previous: Optional[str] = None  # Unified diff string
    
    # Computed metrics
    content_length: int = 0
    word_count: int = 0
    reading_time_minutes: float = 0.0
    
    def __post_init__(self):
        self.content_length = len(self.content)
        self.word_count = len(self.content.split())
        self.reading_time_minutes = max(1, round(self.word_count / 200, 1))  # ~200 wpm


@dataclass
class VersionHistoryEntry:
    """Summary entry in version history timeline"""
    version_number: int
    version_id: str
    author_username: str
    change_summary: str
    created_at: datetime
    content_preview: str
    metrics: Dict[str, Any] = field(default_factory=dict)


class DiffEngine:
    """
    Core engine for computing differences between wiki page versions
    
    Supports multiple diff algorithms and output formats
    """
    
    @staticmethod
    def compute_line_diff(old_content: str, new_content: str) -> DiffResult:
        """
        Compute line-by-line diff between two content strings
        
        Args:
            old_content: Previous version content
            new_content: New version content
            
        Returns:
            DiffResult with detailed change information
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        differ = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile='version_previous',
            tofile='version_current',
            lineterm=''
        )
        
        # Parse unified diff into structured format
        diff_lines = []
        lines_added = 0
        lines_deleted = 0
        lines_modified = 0
        lines_unchanged = 0
        
        # Use SequenceMatcher for more detailed analysis
        matcher = difflib.SequenceMatcher(None, old_lines, new_lines)
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for idx in range(i1, i2):
                    diff_lines.append(DiffLine(
                        line_number=j1 + idx + 1,
                        content=old_lines[idx].rstrip(),
                        change_type=ChangeType.UNCHANGED,
                        old_line_number=i1 + idx + 1
                    ))
                lines_unchanged += (i2 - i1)
                
            elif tag == 'replace':
                # Modified or replaced section
                for idx in range(j1, j2):
                    diff_lines.append(DiffLine(
                        line_number=idx + 1,
                        content=new_lines[idx].rstrip(),
                        change_type=ChangeType.ADDED if j2 - j2 > 0 else ChangeType.MODIFIED,
                        old_line_number=None
                    ))
                
                # Count as modifications if similar length, otherwise add+delete
                old_len = i2 - i1
                new_len = j2 - j1
                if abs(old_len - new_len) <= 2:  # Similar size = modification
                    lines_modified += max(old_len, new_len)
                else:
                    lines_deleted += old_len
                    lines_added += new_len
                    
            elif tag == 'insert':
                for idx in range(j1, j2):
                    diff_lines.append(DiffLine(
                        line_number=idx + 1,
                        content=new_lines[idx].rstrip(),
                        change_type=ChangeType.ADDED
                    ))
                lines_added += (j2 - j1)
                
            elif tag == 'delete':
                for idx in range(i1, i2):
                    diff_lines.append(DiffLine(
                        line_number=-1,  # Deleted lines don't have new number
                        content=old_lines[idx].rstrip(),
                        change_type=ChangeType.DELETED,
                        old_line_number=i1 + idx + 1
                    ))
                lines_deleted += (i2 - i1)
        
        has_changes = (lines_added + lines_deleted + lines_modified) > 0
        
        # Calculate similarity score (0.0 to 1.0)
        total_lines = lines_added + lines_deleted + lines_modified + lines_unchanged
        similarity = lines_unchanged / total_lines if total_lines > 0 else 1.0
        
        # Generate human-readable summary
        summary_parts = []
        if lines_added > 0:
            summary_parts.append(f"+{lines_added} lines added")
        if lines_deleted > 0:
            summary_parts.append(f"-{lines_deleted} lines deleted")
        if lines_modified > 0:
            summary_parts.append(f"~{lines_modified} lines modified")
        
        summary = ", ".join(summary_parts) if summary_parts else "No changes"
        
        return DiffResult(
            version_a=0,  # Will be set by caller
            version_b=0,  # Will be set by caller
            has_changes=has_changes,
            lines_added=lines_added,
            lines_deleted=lines_deleted,
            lines_modified=lines_modified,
            lines_unchanged=lines_unchanged,
            diff_lines=diff_lines,
            summary=summary,
            similarity_score=similarity
        )
    
    @staticmethod
    def compute_word_diff(old_content: str, new_content: str) -> List[Dict]:
        """
        Compute word-level diff for short text segments
        
        Returns list of change hunks with context
        """
        old_words = old_content.split()
        new_words = new_content.split()
        
        matcher = difflib.SequenceMatcher(None, old_words, new_words)
        changes = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                changes.append({
                    "type": tag,
                    "old_text": " ".join(old_words[i1:i2]),
                    "new_text": " ".join(new_words[j1:j2]),
                    "position": i1
                })
        
        return changes
    
    @staticmethod
    def compute_frontmatter_diff(old_fm: Dict, new_fm: Dict) -> Dict[str, Any]:
        """
        Compute structured diff for frontmatter metadata
        
        Returns categorized changes
        """
        all_keys = set(list(old_fm.keys()) + list(new_fm.keys()))
        
        added_keys = []
        deleted_keys = []
        modified_keys = []
        unchanged_keys = []
        
        for key in sorted(all_keys):
            old_val = old_fm.get(key)
            new_val = new_fm.get(key)
            
            if key not in old_fm:
                added_keys.append({
                    "key": key,
                    "value": new_val
                })
            elif key not in new_fm:
                deleted_keys.append({
                    "key": key,
                    "value": old_val
                })
            elif old_val != new_val:
                modified_keys.append({
                    "key": key,
                    "old_value": old_val,
                    "new_value": new_val
                })
            else:
                unchanged_keys.append(key)
        
        return {
            "has_changes": len(added_keys) + len(deleted_keys) + len(modified_keys) > 0,
            "keys_added": added_keys,
            "keys_deleted": deleted_keys,
            "keys_modified": modified_keys,
            "keys_unchanged": unchanged_keys,
            "summary": f"{len(modified_keys)} changed, {len(added_keys)} added, {len(deleted_keys)} removed"
        }
    
    @staticmethod
    def generate_unified_diff(old_content: str, new_content: str,
                              from_label: str = "", to_label: str = "") -> str:
        """
        Generate standard unified diff format string
        
        Useful for storage and external tools compatibility
        """
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=from_label or 'previous',
            tofile=to_label or 'current',
            lineterm=''
        )
        
        return ''.join(diff)
    
    @staticmethod
    def generate_html_diff(diff_result: DiffResult) -> str:
        """
        Generate HTML-formatted diff view for browser rendering
        
        Color-coded display with syntax highlighting
        """
        html_parts = ['<div class="diff-container">']
        html_parts.append('<table class="diff-table">')
        
        for line in diff_result.diff_lines:
            css_class = {
                ChangeType.ADDED: 'diff-added',
                ChangeType.DELETED: 'diff-deleted',
                ChangeType.MODIFIED: 'diff-modified',
                ChangeType.UNCHANGED: 'diff-unchanged'
            }.get(line.change_type, '')
            
            prefix = {
                ChangeType.ADDED: '+',
                ChangeType.DELETED: '-',
                ChangeType.MODIFIED: '~',
                ChangeType.UNCHANGED: ' '
            }.get(line.change_type, ' ')
            
            escaped_content = (
                line.content
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
            )
            
            html_parts.append(f'''
                <tr class="{css_class}">
                    <td class="line-number">{line.old_line_number or ''}</td>
                    <td class="line-number">{line.line_number}</td>
                    <td class="line-content"><span class="prefix">{prefix}</span>{escaped_content}</td>
                </tr>
            ''')
        
        html_parts.append('</table>')
        html_parts.append('</div>')
        
        # Add CSS styles
        css_styles = '''
        <style>
        .diff-container { font-family: monospace; font-size: 13px; }
        .diff-table { width: 100%; border-collapse: collapse; }
        .diff-table td { padding: 2px 8px; vertical-align: top; }
        .line-number { color: #999; width: 40px; text-align: right; user-select: none; }
        .line-content { white-space: pre-wrap; word-break: break-word; }
        .diff-added { background-color: #e6ffed; }
        .diff-deleted { background-color: #ffeef0; }
        .diff-modified { background-color: #fff3cd; }
        .diff-unchanged { color: #666; }
        .prefix { margin-right: 8px; font-weight: bold; }
        </style>
        '''
        
        return css_styles + '\n'.join(html_parts)


class VersionControlManager:
    """
    High-level manager for wiki page version control operations
    
    Provides API-like interface for:
    - Creating new versions
    - Retrieving version history
    - Computing diffs
    - Restoring previous versions
    - Generating version reports
    """
    
    def __init__(self):
        self.diff_engine = DiffEngine()
        self._versions_cache: Dict[str, List[PageVersion]] = {}
    
    def create_version_snapshot(self, page_id: str, version_number: int,
                                content: str, frontmatter: Dict,
                                author_id: str, author_username: str,
                                change_summary: str = "") -> PageVersion:
        """
        Create a new version snapshot of a wiki page
        
        Args:
            page_id: Wiki page identifier
            version_number: Sequential version number
            content: Full page content (Markdown)
            frontmatter: Page metadata dictionary
            author_id: User ID who made the change
            author_username: Display name of author
            change_summary: Human-readable description of changes
            
        Returns:
            Created PageVersion object
        """
        version_id = f"ver_{page_id}_{version_number}"
        
        # Get previous version for diff computation
        previous_version = self.get_latest_version(page_id)
        diff_from_previous = None
        
        if previous_version:
            diff_result = self.diff_engine.compute_line_diff(
                previous_version.content, content
            )
            diff_from_previous = self.diff_engine.generate_unified_diff(
                previous_version.content, content,
                f"v{previous_version.version_number}",
                f"v{version_number}"
            )
        
        version = PageVersion(
            version_id=version_id,
            page_id=page_id,
            version_number=version_number,
            content=content,
            frontmatter=frontmatter,
            author_id=author_id,
            author_username=author_username,
            change_summary=change_summary or f"Updated to v{version_number}",
            created_at=datetime.now(),
            diff_from_previous=diff_from_previous
        )
        
        # Cache the version
        if page_id not in self._versions_cache:
            self._versions_cache[page_id] = []
        self._versions_cache[page_id].append(version)
        
        return version
    
    def get_version_history(self, page_id: str, limit: int = 20) -> List[VersionHistoryEntry]:
        """
        Get version history timeline for a page
        
        Returns summarized entries suitable for UI display
        """
        versions = self._versions_cache.get(page_id, [])
        
        entries = []
        for ver in reversed(versions[-limit:]):
            entry = VersionHistoryEntry(
                version_number=ver.version_number,
                version_id=ver.version_id,
                author_username=ver.author_username,
                change_summary=ver.change_summary,
                created_at=ver.created_at,
                content_preview=ver.content[:150] + "..." if len(ver.content) > 150 else ver.content,
                metrics={
                    "content_length": ver.content_length,
                    "word_count": ver.word_count,
                    "reading_time_minutes": ver.reading_time_minutes
                }
            )
            entries.append(entry)
        
        return entries
    
    def get_version(self, page_id: str, version_number: int) -> Optional[PageVersion]:
        """Get specific version by number"""
        versions = self._versions_cache.get(page_id, [])
        for ver in versions:
            if ver.version_number == version_number:
                return ver
        return None
    
    def get_latest_version(self, page_id: str) -> Optional[PageVersion]:
        """Get most recent version of a page"""
        versions = self._versions_cache.get(page_id, [])
        return versions[-1] if versions else None
    
    def compute_version_diff(self, page_id: str, 
                            version_a: int, 
                            version_b: int) -> Optional[DiffResult]:
        """
        Compute detailed diff between two specific versions
        
        Args:
            page_id: Wiki page identifier
            version_a: Source version number
            version_b: Target version number
            
        Returns:
            DiffResult object with complete change analysis
        """
        ver_a = self.get_version(page_id, version_a)
        ver_b = self.get_version(page_id, version_b)
        
        if not ver_a or not ver_b:
            return None
        
        diff_result = self.diff_engine.compute_line_diff(ver_a.content, ver_b.content)
        diff_result.version_a = version_a
        diff_result.version_b = version_b
        
        return diff_result
    
    def compute_diff_with_previous(self, page_id: str, 
                                  version_number: int) -> Optional[DiffResult]:
        """Compute diff between specified version and its immediate predecessor"""
        if version_number <= 1:
            return None
        
        return self.compute_version_diff(page_id, version_number - 1, version_number)
    
    def generate_version_comparison_report(self, page_id: str) -> Dict:
        """
        Generate comprehensive report comparing all recent versions
        
        Includes statistics, change patterns, and quality metrics
        """
        versions = self._versions_cache.get(page_id, [])
        
        if len(versions) < 2:
            return {"error": "Need at least 2 versions for comparison"}
        
        # Compute consecutive diffs
        diffs = []
        total_changes = 0
        total_additions = 0
        total_deletions = 0
        
        for i in range(1, len(versions)):
            diff = self.diff_engine.compute_line_diff(
                versions[i-1].content, versions[i].content
            )
            # Extract diff attributes (excluding large diff_lines list)
            diff_attrs = {}
            if hasattr(diff, '__dict__'):
                diff_attrs = {
                    k: v for k, v in diff.__dict__.items() 
                    if k != 'diff_lines'
                }
            diffs.append({
                "from_version": versions[i-1].version_number,
                "to_version": versions[i].version_number,
                **diff_attrs
            })
            
            total_changes += diff.lines_added + diff.lines_deleted + diff.lines_modified
            total_additions += diff.lines_added
            total_deletions += diff.lines_deleted
        
        # Author contribution stats
        author_stats = {}
        for ver in versions:
            author = ver.author_username
            if author not in author_stats:
                author_stats[author] = {"edits": 0, "words_added": 0}
            author_stats[author]["edits"] += 1
            author_stats[author]["words_added"] += ver.word_count
        
        # Growth trend
        growth_data = [
            {
                "version": ver.version_number,
                "date": ver.created_at.isoformat(),
                "length": ver.content_length,
                "words": ver.word_count
            }
            for ver in versions
        ]
        
        latest = versions[-1]
        first = versions[0]
        
        return {
            "page_id": page_id,
            "total_versions": len(versions),
            "first_version_date": first.created_at.isoformat(),
            "latest_version_date": latest.created_at.isoformat(),
            "latest_version_number": latest.version_number,
            "total_edits": len(versions) - 1,
            "total_changes_across_versions": total_changes,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "net_growth": latest.content_length - first.content_length,
            "growth_percentage": round(
                ((latest.content_length - first.content_length) / first.content_length * 100)
                if first.content_length > 0 else 0, 1
            ),
            "author_contributions": author_stats,
            "growth_trend": growth_data,
            "recent_diffs": diffs[-5:]  # Last 5 diffs
        }
    
    def restore_version(self, page_id: str, version_number: int,
                       restorer_id: str, restorer_username: str) -> Tuple[Optional[PageVersion], str]:
        """
        Restore a page to a previous version
        
        Creates a new version that copies the restored content
        
        Returns:
            Tuple of (New created version or None, error message)
        """
        target_version = self.get_version(page_id, version_number)
        if not target_version:
            return None, f"Version {version_number} not found"
        
        current_latest = self.get_latest_version(page_id)
        new_version_number = (current_latest.version_number + 1) if current_latest else 1
        
        # Create new version with restored content
        restored_version = self.create_version_snapshot(
            page_id=page_id,
            version_number=new_version_number,
            content=target_version.content,
            frontmatter=target_version.frontmatter.copy(),
            author_id=restorer_id,
            author_username=restorer_username,
            change_summary=f"Restored from v{version_number}"
        )
        
        return restored_version, ""
    
    def get_version_statistics(self, page_id: str = None) -> Dict:
        """
        Get aggregate version control statistics
        
        If page_id provided, returns stats for that page only.
        Otherwise returns system-wide statistics.
        """
        if page_id:
            versions = self._versions_cache.get(page_id, [])
            return self._compute_page_stats(page_id, versions)
        
        # System-wide stats
        all_pages = list(self._versions_cache.keys())
        total_versions = sum(len(v) for v in self._versions_cache.values())
        
        page_stats = []
        for pid in all_pages:
            page_stat = self._compute_page_stats(pid, self._versions_cache[pid])
            page_stats.append(page_stat)
        
        # Find most active pages
        most_active = sorted(page_stats, key=lambda x: x['total_versions'], reverse=True)[:5]
        
        return {
            "system_wide": True,
            "total_pages_tracked": len(all_pages),
            "total_versions_all_pages": total_versions,
            "most_active_pages": most_active,
            "average_versions_per_page": round(total_versions / len(all_pages), 1) if all_pages else 0
        }
    
    def _compute_page_stats(self, page_id: str, versions: List[PageVersion]) -> Dict:
        """Compute statistics for a single page's versions"""
        if not versions:
            return {"page_id": page_id, "total_versions": 0}
        
        total_edits = len(versions) - 1
        unique_authors = len(set(v.author_id for v in versions))
        
        # Calculate edit frequency
        if len(versions) >= 2:
            time_span = (versions[-1].created_at - versions[0].created_at).days
            edits_per_day = total_edits / time_span if time_span > 0 else total_edits
        else:
            edits_per_day = 0
        
        latest = versions[-1]
        
        return {
            "page_id": page_id,
            "total_versions": len(versions),
            "total_edits": total_edits,
            "unique_contributors": unique_authors,
            "edit_frequency_per_day": round(edits_per_day, 2),
            "current_length": latest.content_length,
            "current_word_count": latest.word_count,
            "last_edit_date": latest.created_at.isoformat(),
            "last_editor": latest.author_username
        }


# Global instance
version_control_instance: Optional[VersionControlManager] = None


def get_version_control() -> VersionControlManager:
    """Get or create global version control instance"""
    global version_control_instance
    if version_control_instance is None:
        version_control_instance = VersionControlManager()
    return version_control_instance
