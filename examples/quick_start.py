"""
Octopai 快速入门示例

这个示例展示了如何快速上手使用Octopai项目，围绕着：
- 万物皆可为Skill
- Skill可以在学习中不断自我进化
- 提高AI Agent认知能力
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octopai import Octopai


def example_1_create_from_text():
    """示例1: 从文本创建Skill - 万物皆可为Skill"""
    print("=" * 60)
    print("示例1: 从文本创建Skill - 万物皆可为Skill")
    print("=" * 60)
    
    octopai = Octopai()
    
    # 任何文本内容都可以成为Skill
    text_content = """
    # Python数据处理基础
    
    这是一个关于Python数据处理的Skill。
    
    ## 常用操作
    1. 读取CSV文件
    2. 数据清洗
    3. 数据可视化
    
    ## 示例代码
    ```python
    import pandas as pd
    df = pd.read_csv('data.csv')
    print(df.head())
    ```
    """
    
    print("\n✓ 从文本内容创建Skill")
    skill_def = octopai.skill_factory.create_from_text(
        text=text_content,
        name="Python数据处理",
        description="Python数据处理的基础Skill",
        tags=["python", "data", "tutorial"]
    )
    
    print(f"  Skill ID: {skill_def.metadata.skill_id}")
    print(f"  Skill名称: {skill_def.metadata.name}")
    print(f"  版本: v{skill_def.latest_version.version}")


def example_2_create_from_url():
    """示例2: 从URL创建Skill"""
    print("\n" + "=" * 60)
    print("示例2: 从URL创建Skill")
    print("=" * 60)
    
    octopai = Octopai()
    
    # 注意：这是一个示例，实际使用时需要真实的URL和API密钥
    print("\n✓ 准备从URL创建Skill")
    print("  提示：取消下面代码的注释并填入真实URL即可运行")
    
    # result = octopai.create_from_url(
    #     url="https://example.com/documentation",
    #     name="文档Skill",
    #     description="从网页创建的Skill",
    #     tags=["web", "documentation"]
    # )
    
    print("  功能说明：")
    print("  - 可以将任何网页转换为Skill")
    print("  - 自动提取结构化内容")
    print("  - 支持爬取相关链接")


def example_3_skill_evolution():
    """示例3: Skill自我进化"""
    print("\n" + "=" * 60)
    print("示例3: Skill自我进化")
    print("=" * 60)
    
    octopai = Octopai()
    
    print("\n✓ Skill进化功能说明")
    print("  核心概念：Skill可以在学习中不断自我进化")
    
    # 记录使用情况，为进化做准备
    print("\n  1. 记录Skill使用情况")
    sample_skill_content = "# 示例Skill\n\n这是一个示例Skill的内容。"
    
    octopai.record_skill_usage(
        skill_content=sample_skill_content,
        skill_version=1,
        success=True,
        feedback="这个Skill很有用！",
        performance_metrics={"accuracy": 0.85, "speed": 0.9}
    )
    
    print("     ✓ 使用记录已保存")
    
    # 检查进化准备度
    readiness = octopai.get_evolution_readiness()
    print(f"\n  2. 进化准备度: {readiness}")
    
    print("\n  3. 进化功能特性:")
    print("     - 基于使用反馈自动进化")
    print("     - 多目标优化（可读性、完整性、效率等）")
    print("     - 智能反思和定向改进")
    print("     - 帕累托前沿候选管理")


def example_4_everything_is_a_skill():
    """示例4: 万物皆可为Skill - 展示各种输入类型"""
    print("\n" + "=" * 60)
    print("示例4: 万物皆可为Skill")
    print("=" * 60)
    
    octopai = Octopai()
    
    print("\n✓ Octopai支持从多种来源创建Skill:")
    print("  1. 文本内容 (create_from_text)")
    print("  2. 网页URL (create_from_url)")
    print("  3. 文件 (create_from_files)")
    print("  4. 提示词 (create_from_prompt)")
    print("  5. 代码 (create_from_code)")
    print("  6. API端点 (create_from_api)")
    print("  7. 任何对象 (create_anything)")
    
    # 演示从Python字典创建Skill
    print("\n✓ 演示：从Python字典创建Skill")
    data_dict = {
        "topic": "机器学习",
        "concepts": ["监督学习", "无监督学习", "强化学习"],
        "tools": ["scikit-learn", "TensorFlow", "PyTorch"],
        "examples": 15
    }
    
    skill_def = octopai.skill_factory.create_anything(
        source=data_dict,
        name="机器学习基础",
        description="从字典数据创建的机器学习Skill",
        tags=["ml", "machine-learning", "ai"]
    )
    
    print(f"     ✓ 成功创建Skill: {skill_def.metadata.name}")


def main():
    """运行所有快速入门示例"""
    print("\n" + "=" * 60)
    print("Octopai 快速入门")
    print("=" * 60)
    print("\n核心理念:")
    print("  • 万物皆可为Skill")
    print("  • Skill可以在学习中不断自我进化")
    print("  • 提高AI Agent认知能力")
    
    try:
        example_1_create_from_text()
        example_2_create_from_url()
        example_3_skill_evolution()
        example_4_everything_is_a_skill()
        
        print("\n" + "=" * 60)
        print("✓ 所有示例运行完成！")
        print("=" * 60)
        print("\n下一步建议:")
        print("  1. 配置API密钥 (.env文件)")
        print("  2. 尝试从真实URL创建Skill")
        print("  3. 探索Skill进化功能")
        print("  4. 查看更多示例文件")
        
    except Exception as e:
        print(f"\n✗ 示例运行出错: {e}")
        print("\n提示: 请确保已正确配置API密钥!")


if __name__ == "__main__":
    main()
