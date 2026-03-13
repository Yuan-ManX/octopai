"""
Test cases for SkillHub system
"""

import os
import shutil
import tempfile
import pytest
from exo.core.skill_hub import SkillHub, Skill, SkillVersion, SkillMetadata


class TestSkillVersion:
    """Test SkillVersion class"""
    
    def test_skill_version_creation(self):
        """Test creating a SkillVersion"""
        version = SkillVersion(
            version=1,
            content="# Test Skill\nThis is a test skill",
            author="test-author",
            change_description="Initial version"
        )
        
        assert version.version == 1
        assert "Test Skill" in version.content
        assert version.author == "test-author"
        assert version.change_description == "Initial version"
        assert version.content_hash is not None
    
    def test_skill_version_to_dict(self):
        """Test converting SkillVersion to dict"""
        version = SkillVersion(
            version=1,
            content="# Test",
            author="test"
        )
        
        data = version.to_dict()
        assert data["version"] == 1
        assert data["content"] == "# Test"
        assert data["author"] == "test"
        assert "content_hash" in data
    
    def test_skill_version_from_dict(self):
        """Test creating SkillVersion from dict"""
        data = {
            "version": 2,
            "content": "# Test 2",
            "author": "test2",
            "change_description": "Updated",
            "content_hash": "abc123",
            "created_at": "2026-01-01T00:00:00"
        }
        
        version = SkillVersion.from_dict(data)
        assert version.version == 2
        assert version.content == "# Test 2"
        assert version.author == "test2"


class TestSkillMetadata:
    """Test SkillMetadata class"""
    
    def test_metadata_creation(self):
        """Test creating metadata"""
        metadata = SkillMetadata(
            skill_id="test-skill",
            name="Test Skill",
            description="A test skill",
            tags=["test", "example"],
            category="testing"
        )
        
        assert metadata.skill_id == "test-skill"
        assert metadata.name == "Test Skill"
        assert metadata.tags == ["test", "example"]
        assert metadata.category == "testing"
        assert metadata.usage_count == 0
        assert metadata.success_rate == 0.0
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dict"""
        metadata = SkillMetadata(
            skill_id="test",
            name="Test",
            description="Desc",
            tags=["tag1"],
            category="cat1"
        )
        
        data = metadata.to_dict()
        assert data["skill_id"] == "test"
        assert data["name"] == "Test"
        assert data["tags"] == ["tag1"]


class TestSkill:
    """Test Skill class"""
    
    def test_skill_creation(self):
        """Test creating a Skill"""
        metadata = SkillMetadata(
            skill_id="test-skill",
            name="Test Skill",
            description="A test"
        )
        skill = Skill(metadata)
        
        assert skill.metadata.skill_id == "test-skill"
        assert len(skill.versions) == 0
    
    def test_add_version(self):
        """Test adding versions to a skill"""
        metadata = SkillMetadata(
            skill_id="test-skill",
            name="Test Skill",
            description="A test"
        )
        skill = Skill(metadata)
        
        version1 = skill.add_version("# V1", author="test1", change_description="First version")
        assert version1.version == 1
        
        version2 = skill.add_version("# V2", author="test2", change_description="Second version")
        assert version2.version == 2
        
        assert len(skill.versions) == 2
    
    def test_latest_version(self):
        """Test getting latest version"""
        metadata = SkillMetadata(
            skill_id="test-skill",
            name="Test Skill",
            description="A test"
        )
        skill = Skill(metadata)
        
        skill.add_version("# V1")
        skill.add_version("# V2")
        skill.add_version("# V3")
        
        latest = skill.latest_version
        assert latest is not None
        assert latest.version == 3
        assert latest.content == "# V3"
    
    def test_record_usage(self):
        """Test recording skill usage"""
        metadata = SkillMetadata(
            skill_id="test-skill",
            name="Test Skill",
            description="A test"
        )
        skill = Skill(metadata)
        
        skill.record_usage(success=True)
        assert skill.metadata.usage_count == 1
        assert skill.metadata.success_rate == 1.0
        
        skill.record_usage(success=False)
        assert skill.metadata.usage_count == 2
        assert skill.metadata.success_rate == 0.5


class TestSkillHub:
    """Test SkillHub class"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)
    
    def test_skillhub_creation(self, temp_dir):
        """Test creating SkillHub"""
        hub = SkillHub(temp_dir)
        
        assert hub is not None
        assert os.path.exists(temp_dir)
        assert os.path.exists(os.path.join(temp_dir, "skills"))
    
    def test_create_skill(self, temp_dir):
        """Test creating a skill in SkillHub"""
        hub = SkillHub(temp_dir)
        
        skill = hub.create_skill(
            name="Data Analysis",
            description="Analyze CSV data",
            content="# Data Analysis\nThis skill analyzes CSV files.",
            tags=["data", "csv"],
            category="analysis"
        )
        
        assert skill is not None
        assert skill.metadata.name == "Data Analysis"
        assert "data-analysis" in skill.metadata.skill_id
        assert len(skill.versions) == 1
    
    def test_get_skill(self, temp_dir):
        """Test getting a skill from SkillHub"""
        hub = SkillHub(temp_dir)
        
        created = hub.create_skill(
            name="Test Skill",
            description="Test",
            content="# Test"
        )
        
        retrieved = hub.get_skill(created.metadata.skill_id)
        
        assert retrieved is not None
        assert retrieved.metadata.skill_id == created.metadata.skill_id
    
    def test_update_skill(self, temp_dir):
        """Test updating a skill in SkillHub"""
        hub = SkillHub(temp_dir)
        
        created = hub.create_skill(
            name="Test Skill",
            description="Test",
            content="# V1"
        )
        
        updated = hub.update_skill(
            skill_id=created.metadata.skill_id,
            content="# V2 - Updated",
            author="tester",
            change_description="Updated version"
        )
        
        assert updated is not None
        assert updated.latest_version is not None
        assert updated.latest_version.version == 2
        assert "V2" in updated.latest_version.content
    
    def test_search_skills(self, temp_dir):
        """Test searching skills in SkillHub"""
        hub = SkillHub(temp_dir)
        
        hub.create_skill(
            name="Data Analysis",
            description="Analyze data files",
            content="# Data Analysis",
            tags=["data", "csv"]
        )
        
        hub.create_skill(
            name="Web Scraping",
            description="Scrape web pages",
            content="# Web Scraping",
            tags=["web", "scraping"]
        )
        
        results = hub.search_skills("data")
        assert len(results) >= 1
        assert any("Data Analysis" in r.metadata.name for r in results)
    
    def test_list_skills(self, temp_dir):
        """Test listing skills in SkillHub"""
        hub = SkillHub(temp_dir)
        
        hub.create_skill("Skill 1", "Desc 1", "# 1", category="cat1")
        hub.create_skill("Skill 2", "Desc 2", "# 2", category="cat1")
        hub.create_skill("Skill 3", "Desc 3", "# 3", category="cat2")
        
        all_skills = hub.list_skills()
        assert len(all_skills) == 3
        
        cat1_skills = hub.list_skills(category="cat1")
        assert len(cat1_skills) == 2
    
    def test_merge_skills(self, temp_dir):
        """Test merging skills"""
        hub = SkillHub(temp_dir)
        
        skill1 = hub.create_skill(
            name="CSV Reader",
            description="Read CSV files",
            content="# CSV Reader\nRead CSV files.",
            tags=["csv", "read"]
        )
        
        skill2 = hub.create_skill(
            name="Data Cleaner",
            description="Clean data",
            content="# Data Cleaner\nClean data.",
            tags=["clean", "data"]
        )
        
        merged = hub.merge_skills(
            skill_ids=[skill1.metadata.skill_id, skill2.metadata.skill_id],
            new_name="CSV Processing",
            new_description="Read and clean CSV data"
        )
        
        assert merged is not None
        assert merged.metadata.name == "CSV Processing"
        assert "csv" in merged.metadata.tags
        assert "read" in merged.metadata.tags
        assert "clean" in merged.metadata.tags
    
    def test_get_statistics(self, temp_dir):
        """Test getting SkillHub statistics"""
        hub = SkillHub(temp_dir)
        
        hub.create_skill("Skill 1", "Desc 1", "# 1", category="cat1")
        hub.create_skill("Skill 2", "Desc 2", "# 2", category="cat1")
        
        stats = hub.get_statistics()
        
        assert stats["total_skills"] == 2
        assert stats["total_versions"] == 2
        assert "categories" in stats
        assert stats["categories"]["cat1"] == 2
