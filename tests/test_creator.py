import os
import tempfile
from octopai.core.creator import SkillCreator


def test_creator_initialization():
    """测试创建器初始化"""
    creator = SkillCreator()
    assert creator is not None


def test_create_skill():
    """测试创建skill"""
    # 注意：这个测试需要真实的API密钥才能运行
    # 这里只测试基本功能，不实际调用API
    creator = SkillCreator()
    assert hasattr(creator, 'create')
