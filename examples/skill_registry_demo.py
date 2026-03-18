"""
Octopai Skill Registry - 示例演示

本示例展示 Octopai 的高级技能注册表系统，包括：
- 技能发布和版本管理
- Slug 管理和重定向
- 技能重命名和合并
- 软删除和恢复
- 星级评分和评论
- 安装统计和搜索发现
"""

from octopai import Octopai


def main():
    print("=" * 70)
    print("Octopai 技能注册表系统 - 示例演示")
    print("=" * 70)
    
    # 初始化 Octopai
    octopai = Octopai()
    print("\n[1] Octopai 系统初始化完成")
    
    # ==================== 第1部分：技能发布 ====================
    print("\n" + "=" * 70)
    print("[2] 技能发布 - Skill Publishing")
    print("=" * 70)
    
    user_id = "user-001"
    
    # 发布第一个技能
    print("\n2.1 发布第一个技能...")
    skill1 = octopai.publish_skill_to_registry(
        name="数据可视化工具",
        description="创建美观的数据可视化图表的技能",
        version="1.0.0",
        author="张三",
        owner_id=user_id,
        tags=["数据可视化", "图表", "数据分析"],
        category="data-visualization",
        visibility="public",
        license="MIT",
        changelog_entry="初始版本发布"
    )
    print(f"   ✓ 技能已发布: {skill1.name}")
    print(f"   - Slug: {skill1.slug}")
    print(f"   - 版本: {skill1.version}")
    
    # 发布第二个技能
    print("\n2.2 发布第二个技能...")
    skill2 = octopai.publish_skill_to_registry(
        name="数据清洗工具",
        description="清洗和预处理数据的技能",
        version="1.0.0",
        author="李四",
        owner_id=user_id,
        tags=["数据清洗", "预处理", "数据质量"],
        category="data-preprocessing",
        visibility="public",
        license="MIT",
        changelog_entry="初始版本发布"
    )
    print(f"   ✓ 技能已发布: {skill2.name}")
    print(f"   - Slug: {skill2.slug}")
    
    # 发布第三个技能（用于合并演示）
    print("\n2.3 发布第三个技能（重复）...")
    skill3 = octopai.publish_skill_to_registry(
        name="数据可视化助手",
        description="帮助创建数据可视化的技能",
        version="1.0.0",
        author="张三",
        owner_id=user_id,
        tags=["数据可视化", "图表"],
        category="data-visualization",
        visibility="public",
        license="MIT",
        changelog_entry="初始版本发布"
    )
    print(f"   ✓ 技能已发布: {skill3.name}")
    print(f"   - Slug: {skill3.slug}")
    
    # ==================== 第2部分：版本更新 ====================
    print("\n" + "=" * 70)
    print("[3] 版本更新 - Version Updates")
    print("=" * 70)
    
    print("\n3.1 更新技能版本...")
    updated_skill = octopai.update_registry_skill_version(
        skill_id=skill1.skill_id,
        new_version="1.1.0",
        changelog_entry="添加了新的图表类型和优化",
        user_id=user_id
    )
    if updated_skill:
        print(f"   ✓ 技能已更新: {updated_skill.name}")
        print(f"   - 新版本: {updated_skill.version}")
        print(f"   - 更新日志: {updated_skill.changelog[0]['changes']}")
    
    # ==================== 第3部分：Slug 和重定向 ====================
    print("\n" + "=" * 70)
    print("[4] Slug 管理和重定向 - Slug & Redirects")
    print("=" * 70)
    
    print("\n4.1 重命名技能...")
    old_slug = skill2.slug
    renamed_skill = octopai.rename_registry_skill(
        skill_id=skill2.skill_id,
        new_name="数据预处理工具",
        user_id=user_id
    )
    if renamed_skill:
        print(f"   ✓ 技能已重命名")
        print(f"   - 旧 Slug: {old_slug}")
        print(f"   - 新 Slug: {renamed_skill.slug}")
        print(f"   - 新名称: {renamed_skill.name}")
        
        # 验证重定向
        print("\n4.2 验证重定向...")
        found_by_old = octopai.get_registry_skill_by_slug(old_slug)
        if found_by_old:
            print(f"   ✓ 通过旧 Slug 仍能找到技能: {found_by_old.name}")
    
    # ==================== 第4部分：技能合并 ====================
    print("\n" + "=" * 70)
    print("[5] 技能合并 - Skill Merging")
    print("=" * 70)
    
    print("\n5.1 合并重复技能...")
    merge_success = octopai.merge_registry_skills(
        source_slug=skill3.slug,
        target_slug=skill1.slug,
        user_id=user_id
    )
    if merge_success:
        print(f"   ✓ 技能合并成功")
        print(f"   - 源 Slug: {skill3.slug}")
        print(f"   - 目标 Slug: {skill1.slug}")
        
        # 验证源技能已被隐藏
        merged_skill = octopai.get_registry_skill_by_id(skill3.skill_id)
        if merged_skill:
            print(f"   - 源技能状态: {merged_skill.status.value}")
    
    # ==================== 第5部分：社交互动 ====================
    print("\n" + "=" * 70)
    print("[6] 社交互动 - Social Interactions")
    print("=" * 70)
    
    # 星级评分
    print("\n6.1 添加星级评分...")
    user2_id = "user-002"
    star = octopai.star_registry_skill(
        skill_id=skill1.skill_id,
        user_id=user2_id,
        rating=5.0
    )
    print(f"   ✓ 评分已添加: {star.rating} 星")
    
    # 另一个用户评分
    user3_id = "user-003"
    octopai.star_registry_skill(
        skill_id=skill1.skill_id,
        user_id=user3_id,
        rating=4.5
    )
    
    # 查看更新后的技能
    updated_skill1 = octopai.get_registry_skill_by_id(skill1.skill_id)
    if updated_skill1:
        print(f"   - 总评分人数: {updated_skill1.star_count}")
        print(f"   - 平均评分: {updated_skill1.average_rating:.1f}")
    
    # 添加评论
    print("\n6.2 添加评论...")
    comment = octopai.add_comment_to_registry_skill(
        skill_id=skill1.skill_id,
        author="王五",
        content="这个技能非常好用，图表效果很棒！"
    )
    print(f"   ✓ 评论已添加")
    print(f"   - 作者: {comment.author}")
    print(f"   - 内容: {comment.content}")
    
    # ==================== 第6部分：安装统计 ====================
    print("\n" + "=" * 70)
    print("[7] 安装统计 - Installation Tracking")
    print("=" * 70)
    
    print("\n7.1 记录技能安装...")
    for i in range(5):
        install = octopai.record_registry_skill_install(
            skill_id=skill1.skill_id,
            slug=skill1.slug,
            version=skill1.version,
            installed_by=f"user-{i+10}",
            is_local=True
        )
        print(f"   ✓ 安装记录 {i+1}: {install.installed_by}")
    
    # 查看更新后的安装数
    updated_skill1 = octopai.get_registry_skill_by_id(skill1.skill_id)
    if updated_skill1:
        print(f"\n   - 总安装数: {updated_skill1.install_count}")
    
    # ==================== 第7部分：搜索发现 ====================
    print("\n" + "=" * 70)
    print("[8] 搜索发现 - Search & Discovery")
    print("=" * 70)
    
    print("\n8.1 搜索技能...")
    results = octopai.search_registry_skills(
        query="数据",
        sort_by="popular",
        limit=10
    )
    print(f"   ✓ 找到 {len(results)} 个技能:")
    for skill in results:
        print(f"   - {skill.name} (安装: {skill.install_count}, 评分: {skill.average_rating:.1f})")
    
    print("\n8.2 获取热门技能...")
    popular = octopai.get_popular_registry_skills(limit=5)
    print(f"   ✓ 热门技能:")
    for skill in popular:
        print(f"   - {skill.name} (Slug: {skill.slug})")
    
    # ==================== 第8部分：软删除和恢复 ====================
    print("\n" + "=" * 70)
    print("[9] 软删除和恢复 - Soft Delete & Restore")
    print("=" * 70)
    
    print("\n9.1 软删除技能...")
    delete_success = octopai.soft_delete_registry_skill(
        skill_id=skill2.skill_id,
        user_id=user_id
    )
    if delete_success:
        print(f"   ✓ 技能已软删除")
        deleted_skill = octopai.get_registry_skill_by_id(skill2.skill_id)
        if deleted_skill:
            print(f"   - 状态: {deleted_skill.status.value}")
    
    print("\n9.2 恢复技能...")
    restore_success = octopai.restore_registry_skill(
        skill_id=skill2.skill_id,
        user_id=user_id
    )
    if restore_success:
        print(f"   ✓ 技能已恢复")
        restored_skill = octopai.get_registry_skill_by_id(skill2.skill_id)
        if restored_skill:
            print(f"   - 状态: {restored_skill.status.value}")
    
    # ==================== 第9部分：统计信息 ====================
    print("\n" + "=" * 70)
    print("[10] 注册表统计 - Registry Statistics")
    print("=" * 70)
    
    stats = octopai.get_registry_statistics()
    print(f"\n   总技能数: {stats['total_skills']}")
    print(f"   活跃技能: {stats['active_skills']}")
    print(f"   已删除技能: {stats['deleted_skills']}")
    print(f"   总安装数: {stats['total_installs']}")
    print(f"   总评分数: {stats['total_stars']}")
    print(f"   总评论数: {stats['total_comments']}")
    print(f"   重定向数: {stats['total_redirects']}")
    print(f"   分类统计: {stats['categories']}")
    
    # ==================== 总结 ====================
    print("\n" + "=" * 70)
    print("[11] 示例完成")
    print("=" * 70)
    print("\n本示例展示了 Octopai 技能注册表的核心创新功能：")
    print("\n1. 技能发布与版本管理")
    print("   - 标准化的技能元数据")
    print("   - 语义化版本控制")
    print("   - 更新日志记录")
    print("\n2. Slug 管理与重定向")
    print("   - URL 友好的技能标识")
    print("   - 重命名不破坏旧链接")
    print("   - 智能重定向系统")
    print("\n3. 技能合并")
    print("   - 重复技能规范化")
    print("   - 保留历史访问")
    print("   - 统一管理入口")
    print("\n4. 软删除与恢复")
    print("   - 安全的删除机制")
    print("   - 可恢复的删除操作")
    print("   - 权限控制保护")
    print("\n5. 社交互动")
    print("   - 星级评分系统")
    print("   - 评论与反馈")
    print("   - 社区驱动的质量信号")
    print("\n6. 安装跟踪")
    print("   - 安装统计")
    print("   - 流行度排名")
    print("   - 使用洞察")
    print("\n7. 搜索发现")
    print("   - 多维度搜索")
    print("   - 智能排序")
    print("   - 分类筛选")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
