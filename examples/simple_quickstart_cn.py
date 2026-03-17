"""
Octopai 简单快速入门 - 核心功能
====================================
一个简单易用的脚本，展示Octopai的核心功能。
您可以直接运行它，或者将其集成到您自己的项目中！
"""

import os
import sys

# 将项目根目录添加到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from octopai import (
    Octopai,
    create_from_prompt,
    create_from_text,
    parse,
    hub_create,
    hub_list,
    hub_search,
    hub_stats,
    hub_create_collection,
    hub_semantic_search,
    hub_publish,
    hub_add_rating,
    get_insights
)


def section_header(title):
    """打印章节标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_1_basic_initialization():
    """演示1：基础初始化"""
    section_header("1. 基础初始化")
    print("正在初始化Octopai...")
    
    # 使用默认设置初始化Octopai
    octopai = Octopai()
    print("✓ Octopai初始化成功！")
    print("  - 您已准备好使用所有Octopai功能")
    print("  - 技能将存储在 ./SkillHub 目录中")
    return octopai


def demo_2_create_from_prompt():
    """演示2：从简单提示创建技能"""
    section_header("2. 从提示创建技能")
    print("正在从简单描述创建技能...")
    
    # 使用简单的便捷函数创建技能
    skill = create_from_prompt(
        prompt="创建一个生成Python单元测试的技能",
        name="Python单元测试生成器",
        description="为Python函数生成全面的单元测试",
        tags=["python", "测试", "单元测试"],
        category="开发"
    )
    
    print(f"✓ 技能已创建！")
    print(f"  名称：{skill.metadata.name}")
    print(f"  版本：v{skill.latest_version.version}")
    return skill


def demo_3_create_from_text():
    """演示3：从文本内容创建技能"""
    section_header("3. 从文本创建技能")
    print("正在从原始文本内容创建技能...")
    
    # 任何文本都可以成为技能！
    text_content = """
    # 数据可视化最佳实践
    
    ## 关键原则
    1. 保持简单和专注
    2. 使用适当的图表类型
    3. 清晰地标注所有内容
    4. 有策略地使用颜色
    
    ## 常见图表类型
    - 条形图：比较类别
    - 折线图：显示随时间的趋势
    - 散点图：显示相关性
    """
    
    skill = create_from_text(
        text=text_content,
        name="数据可视化指南",
        description="创建有效数据可视化的最佳实践",
        tags=["可视化", "数据", "设计"],
        category="数据科学"
    )
    
    print(f"✓ 从文本创建技能成功！")
    print(f"  名称：{skill.metadata.name}")
    print(f"  类别：{skill.metadata.category}")
    return skill


def demo_4_skill_hub_basics(octopai):
    """演示4：SkillHub基础 - 创建、列表、搜索"""
    section_header("4. SkillHub - 管理您的技能")
    
    # 在SkillHub中创建技能
    print("\n正在SkillHub中创建技能...")
    skill = hub_create(
        name="CSV数据分析器",
        description="分析和可视化CSV数据文件",
        prompt="创建一个用于处理CSV数据的全面技能",
        tags=["csv", "数据", "分析"],
        category="数据处理"
    )
    
    print(f"✓ 技能已在SkillHub中创建！")
    print(f"  技能ID：{skill.metadata.skill_id}")
    skill_id = skill.metadata.skill_id
    
    # 列出所有技能
    print("\n正在列出SkillHub中的所有技能...")
    all_skills = hub_list()
    print(f"✓ 找到 {len(all_skills)} 个技能")
    for i, s in enumerate(all_skills[:3], 1):
        print(f"  {i}. {s.name}")
    
    # 搜索技能
    print("\n正在搜索'data'技能...")
    search_results = hub_search("数据", category="数据处理")
    print(f"✓ 找到 {len(search_results)} 个匹配的技能")
    
    # 获取统计信息
    print("\n正在获取SkillHub统计信息...")
    stats = hub_stats()
    print(f"✓ 统计信息：")
    print(f"  总技能数：{stats.get('total_skills', 0)}")
    print(f"  总类别数：{stats.get('total_categories', 0)}")
    
    return skill_id


def demo_5_collections_and_organization(skill_id):
    """演示5：将技能组织到集合中"""
    section_header("5. 技能集合 - 组织您的技能")
    
    # 创建集合
    print("\n正在创建技能集合...")
    collection = hub_create_collection(
        name="数据科学工具包",
        description="数据科学工作的必备技能",
        skill_ids=[skill_id],
        tags=["数据科学", "工具", "必备"]
    )
    
    print(f"✓ 集合已创建！")
    print(f"  名称：{collection.name}")
    print(f"  集合中的技能数：{len(collection.skill_ids)}")
    
    # 列出所有集合
    print("\n正在列出所有集合...")
    collections = hub_list_collections()
    print(f"✓ 找到 {len(collections)} 个集合")
    return collection.collection_id


def demo_6_semantic_search_and_publishing(skill_id):
    """演示6：语义搜索和发布工作流"""
    section_header("6. 语义搜索和发布")
    
    # 语义搜索（比关键词搜索更智能）
    print("\n正在执行语义搜索...")
    semantic_results = hub_semantic_search(
        "分析电子表格文件",
        category="数据处理"
    )
    print(f"✓ 语义搜索找到 {len(semantic_results)} 个结果")
    for i, (skill, score) in enumerate(semantic_results[:3], 1):
        print(f"  {i}. {skill.name} (相关性：{score:.2f})")
    
    # 发布技能
    print("\n正在发布技能...")
    published = hub_publish(skill_id)
    if published:
        print(f"✓ 技能已发布！")
        print(f"  状态：{published.metadata.status}")
        print(f"  可见性：{published.metadata.visibility}")
    
    # 添加评分
    print("\n正在为技能添加评分...")
    rating = hub_add_rating(
        skill_id=skill_id,
        rating=5.0,
        feedback="这个技能对CSV分析非常有用！",
        reviewer="用户"
    )
    if rating:
        print(f"✓ 评分已添加！")
        print(f"  评分：{rating.rating}/5.0")


def demo_7_everything_is_a_skill(octopai):
    """演示7：展示'万物皆可为Skill'的理念"""
    section_header("7. 万物皆可为Skill！")
    
    print("Octopai可以将任何东西转化为技能：")
    print("  - 文本内容 ✓")
    print("  - 网页URL ✓")
    print("  - 文件（PDF、DOC、Excel等）✓")
    print("  - 代码片段 ✓")
    print("  - 提示和想法 ✓")
    print("  - 甚至Python字典和对象！✓")
    
    # 示例：从Python字典创建
    print("\n正在从Python字典创建技能...")
    data_dict = {
        "主题": "机器学习算法",
        "类型": ["监督学习", "无监督学习", "强化学习"],
        "示例": ["回归", "分类", "聚类"],
        "工具": ["scikit-learn", "TensorFlow", "PyTorch"]
    }
    
    skill = octopai.create_anything(
        source=data_dict,
        name="ML算法概览",
        description="机器学习算法类型的快速参考",
        tags=["机器学习", "算法", "参考"],
        category="人工智能"
    )
    
    print(f"✓ 从字典创建技能成功！")
    print(f"  名称：{skill.metadata.name}")


def demo_8_integration_pattern():
    """演示8：如何将Octopai集成到您自己的项目中"""
    section_header("8. 将Octopai集成到您的项目中")
    
    print("Octopai设计为可以轻松集成到任何Python项目中！")
    print("\n示例模式：")
    
    print("\n模式1：使用便捷函数（最简单）")
    print("""
    from octopai import create_from_prompt, hub_create, hub_search
    
    # 创建技能
    skill = create_from_prompt(
        prompt="为我的任务创建一个技能",
        name="我的技能",
        description="做一些很棒的事情"
    )
    
    # 搜索现有技能
    results = hub_search("任务自动化")
    """)
    
    print("\n模式2：使用Octopai类（更多控制）")
    print("""
    from octopai import Octopai
    
    # 使用自定义设置初始化
    octopai = Octopai(
        skill_hub_dir="./my_skills",
        experience_dir="./my_experiences"
    )
    
    # 通过实例使用所有功能
    skill = octopai.create_skill_in_hub(
        name="自定义技能",
        description="我的自定义技能",
        prompt="创建一些特殊的东西"
    )
    """)
    
    print("\n模式3：只导入您需要的内容")
    print("""
    from octopai import hub_list, hub_stats, hub_semantic_search
    
    # 只使用SkillHub功能
    skills = hub_list(category="数据科学")
    stats = hub_stats()
    results = hub_semantic_search("机器学习")
    """)


def demo_9_get_insights():
    """演示9：获取体验洞察"""
    section_header("9. 体验与洞察")
    
    print("Octopai跟踪技能使用情况并提供洞察！")
    print("\n正在获取洞察...")
    
    insights = get_insights()
    print(f"✓ 可用的洞察：")
    print(f"  总交互次数：{insights.get('total_interactions', 0)}")
    print(f"  成功率：{insights.get('success_rate', 0):.1%}")


def main():
    """运行所有演示"""
    print("\n" + "="*70)
    print("  🐙 Octopai - 简单快速入门")
    print("="*70)
    print("\n欢迎使用Octopai！")
    print("这个脚本将以简单的步骤演示所有核心功能。")
    print("您可以将这些模式直接复制到您自己的项目中！")
    
    try:
        # 运行所有演示
        octopai = demo_1_basic_initialization()
        demo_2_create_from_prompt()
        demo_3_create_from_text()
        skill_id = demo_4_skill_hub_basics(octopai)
        demo_5_collections_and_organization(skill_id)
        demo_6_semantic_search_and_publishing(skill_id)
        demo_7_everything_is_a_skill(octopai)
        demo_8_integration_pattern()
        demo_9_get_insights()
        
        # 总结
        print("\n" + "="*70)
        print("  ✓ 所有演示成功完成！")
        print("="*70)
        print("\n下一步：")
        print("  1. 探索examples目录以获取更多高级用法")
        print("  2. 查看README获取完整文档")
        print("  3. 尝试用真实内容创建自己的技能")
        print("  4. 将Octopai集成到您的项目中！")
        print("\n记住：万物皆可为Skill！🐙")
        
    except Exception as e:
        print(f"\n✗ 错误：{e}")
        print("\n注意：某些功能可能需要API密钥才能完全使用。")
        print("检查.env.example文件进行配置。")


if __name__ == "__main__":
    main()
