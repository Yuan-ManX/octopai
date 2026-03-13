"""
Tests for Resource Parser module

Tests the parsing capabilities for various file formats.
"""

import os
import tempfile
import pytest
from exo.core.resource_parser import (
    ResourceParser,
    ParsedResource,
    ResourceType,
    parse_resource,
    parse_to_skill_resource,
    TextParser,
    PDFParser,
    DOCParser,
    ExcelParser,
    ImageParser,
    HTMLParser
)


class TestResourceType:
    """Tests for ResourceType enum"""
    
    def test_resource_type_values(self):
        """Test that all resource types have correct values"""
        assert ResourceType.PDF.value == "pdf"
        assert ResourceType.DOC.value == "doc"
        assert ResourceType.DOCX.value == "docx"
        assert ResourceType.EXCEL.value == "excel"
        assert ResourceType.IMAGE.value == "image"
        assert ResourceType.VIDEO.value == "video"
        assert ResourceType.TEXT.value == "text"
        assert ResourceType.MARKDOWN.value == "markdown"
        assert ResourceType.HTML.value == "html"
        assert ResourceType.UNKNOWN.value == "unknown"


class TestParsedResource:
    """Tests for ParsedResource class"""
    
    def test_initialization(self):
        """Test basic initialization"""
        resource = ParsedResource(
            file_path="test.txt",
            resource_type=ResourceType.TEXT,
            text_content="Hello, World!",
            metadata={"key": "value"}
        )
        
        assert resource.file_path == "test.txt"
        assert resource.resource_type == ResourceType.TEXT
        assert resource.text_content == "Hello, World!"
        assert resource.metadata == {"key": "value"}
        assert resource.images == []
    
    def test_to_skill_resource(self):
        """Test conversion to skill resource format"""
        resource = ParsedResource(
            file_path="test.txt",
            resource_type=ResourceType.TEXT,
            text_content="Test content",
            metadata={"author": "test", "size": 100}
        )
        
        skill_resource = resource.to_skill_resource()
        
        assert "# Resource: test.txt" in skill_resource
        assert "Type: text" in skill_resource
        assert "## Metadata" in skill_resource
        assert "author: test" in skill_resource
        assert "size: 100" in skill_resource
        assert "## Content" in skill_resource
        assert "Test content" in skill_resource
    
    def test_get_base64_images(self):
        """Test base64 image encoding"""
        test_image = b"test_image_data"
        resource = ParsedResource(
            file_path="test.jpg",
            resource_type=ResourceType.IMAGE,
            text_content="Image file",
            metadata={},
            images=[test_image]
        )
        
        base64_images = resource.get_base64_images()
        assert len(base64_images) == 1
        import base64
        assert base64_images[0] == base64.b64encode(test_image).decode('utf-8')


class TestTextParser:
    """Tests for TextParser"""
    
    def test_can_parse_text_files(self):
        """Test that text parser can handle various text formats"""
        parser = TextParser()
        
        assert parser.can_parse("test.txt") is True
        assert parser.can_parse("test.md") is True
        assert parser.can_parse("test.markdown") is True
        assert parser.can_parse("test.csv") is True
        assert parser.can_parse("test.json") is True
        assert parser.can_parse("test.yaml") is True
        assert parser.can_parse("test.yml") is True
        assert parser.can_parse("test.pdf") is False
    
    def test_parse_text_file(self):
        """Test parsing a text file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello, World!\nThis is a test.")
            temp_path = f.name
        
        try:
            parser = TextParser()
            result = parser.parse(temp_path)
            
            assert result.resource_type == ResourceType.TEXT
            assert "Hello, World!" in result.text_content
            assert "This is a test." in result.text_content
            assert "file_size" in result.metadata
        finally:
            os.unlink(temp_path)
    
    def test_parse_markdown_file(self):
        """Test parsing a markdown file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Heading\n\nSome **bold** text.")
            temp_path = f.name
        
        try:
            parser = TextParser()
            result = parser.parse(temp_path)
            
            assert result.resource_type == ResourceType.MARKDOWN
            assert "# Heading" in result.text_content
        finally:
            os.unlink(temp_path)


class TestHTMLParser:
    """Tests for HTMLParser"""
    
    def test_can_parse_html_files(self):
        """Test that HTML parser can handle HTML files"""
        parser = HTMLParser()
        
        assert parser.can_parse("test.html") is True
        assert parser.can_parse("test.htm") is True
        assert parser.can_parse("test.txt") is False
    
    def test_parse_html_file(self):
        """Test parsing an HTML file"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Test Page</title></head>
        <body>
            <h1>Hello</h1>
            <p>This is a test.</p>
        </body>
        </html>
        """
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            temp_path = f.name
        
        try:
            parser = HTMLParser()
            result = parser.parse(temp_path)
            
            assert result.resource_type == ResourceType.HTML
            assert "file_size" in result.metadata
        finally:
            os.unlink(temp_path)


class TestPDFParser:
    """Tests for PDFParser"""
    
    def test_can_parse_pdf_files(self):
        """Test that PDF parser can handle PDF files"""
        parser = PDFParser()
        
        assert parser.can_parse("test.pdf") is True
        assert parser.can_parse("test.PDF") is True
        assert parser.can_parse("test.txt") is False


class TestDOCParser:
    """Tests for DOCParser"""
    
    def test_can_parse_doc_files(self):
        """Test that DOC parser can handle DOC/DOCX files"""
        parser = DOCParser()
        
        assert parser.can_parse("test.doc") is True
        assert parser.can_parse("test.docx") is True
        assert parser.can_parse("test.DOCX") is True
        assert parser.can_parse("test.txt") is False


class TestExcelParser:
    """Tests for ExcelParser"""
    
    def test_can_parse_excel_files(self):
        """Test that Excel parser can handle Excel files"""
        parser = ExcelParser()
        
        assert parser.can_parse("test.xlsx") is True
        assert parser.can_parse("test.xls") is True
        assert parser.can_parse("test.csv") is True
        assert parser.can_parse("test.txt") is False


class TestImageParser:
    """Tests for ImageParser"""
    
    def test_can_parse_image_files(self):
        """Test that Image parser can handle various image formats"""
        parser = ImageParser()
        
        assert parser.can_parse("test.jpg") is True
        assert parser.can_parse("test.jpeg") is True
        assert parser.can_parse("test.png") is True
        assert parser.can_parse("test.gif") is True
        assert parser.can_parse("test.bmp") is True
        assert parser.can_parse("test.webp") is True
        assert parser.can_parse("test.tiff") is True
        assert parser.can_parse("test.txt") is False


class TestResourceParser:
    """Tests for main ResourceParser class"""
    
    def test_parse_text_file(self):
        """Test parsing a text file through main parser"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test content")
            temp_path = f.name
        
        try:
            parser = ResourceParser()
            result = parser.parse(temp_path)
            
            assert isinstance(result, ParsedResource)
            assert result.resource_type == ResourceType.TEXT
        finally:
            os.unlink(temp_path)
    
    def test_parse_nonexistent_file(self):
        """Test that parsing nonexistent file raises error"""
        parser = ResourceParser()
        
        with pytest.raises(FileNotFoundError):
            parser.parse("nonexistent_file_1234.txt")
    
    def test_parse_unknown_file_type(self):
        """Test parsing an unknown file type"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz123', delete=False) as f:
            f.write("Test")
            temp_path = f.name
        
        try:
            parser = ResourceParser()
            result = parser.parse(temp_path)
            
            assert result.resource_type == ResourceType.UNKNOWN
        finally:
            os.unlink(temp_path)
    
    def test_parse_to_skill_resource(self):
        """Test parsing directly to skill resource format"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Skill resource content")
            temp_path = f.name
        
        try:
            parser = ResourceParser()
            result = parser.parse_to_skill_resource(temp_path)
            
            assert isinstance(result, str)
            assert "# Resource:" in result
        finally:
            os.unlink(temp_path)


class TestConvenienceFunctions:
    """Tests for convenience functions"""
    
    def test_parse_resource(self):
        """Test parse_resource convenience function"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test")
            temp_path = f.name
        
        try:
            result = parse_resource(temp_path)
            assert isinstance(result, ParsedResource)
        finally:
            os.unlink(temp_path)
    
    def test_parse_to_skill_resource_func(self):
        """Test parse_to_skill_resource convenience function"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test")
            temp_path = f.name
        
        try:
            result = parse_to_skill_resource(temp_path)
            assert isinstance(result, str)
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
