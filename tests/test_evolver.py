import os
import tempfile
from exo.core.evolver import SkillEvolver


def test_evolver_initialization():
    """测试进化器初始化"""
    evolver = SkillEvolver()
    assert evolver is not None


def test_evolve_skill():
    """测试进化skill"""
    # 注意：这个测试需要真实的API密钥才能运行
    # 这里只测试基本功能，不实际调用API
    evolver = SkillEvolver()
    assert hasattr(evolver, 'evolve')
