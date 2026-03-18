"""
Octopai Advanced Skill Evolution - 示例演示

本示例展示 Octopai 的高级技能进化系统，包括：
- 分层技能库管理
- 经验驱动的技能提炼
- 递归技能进化机制
"""

from octopai import Octopai
from octopai.core.experience_distiller import TrajectoryType
from octopai.core.recursive_evolution import EvolutionTrigger


def main():
    print("=" * 70)
    print("Octopai 高级技能进化系统 - 示例演示")
    print("=" * 70)
    
    # 初始化 Octopai
    octopai = Octopai()
    print("\n[1] Octopai 系统初始化完成")
    
    # ==================== 第1部分：分层技能库 ====================
    print("\n" + "=" * 70)
    print("[2] 分层技能库 - SkillBank")
    print("=" * 70)
    
    # 添加通用技能
    print("\n2.1 添加通用技能...")
    general_skill = octopai.add_general_skill_to_bank(
        name="问题分析框架",
        description="通用的问题分析方法论",
        content="""# 问题分析框架

## 核心原则
1. 先理解问题，再寻找解决方案
2. 将复杂问题分解为可管理的子问题
3. 识别问题的根本原因，而非表面现象
4. 验证假设，避免过早下结论

## 分析步骤
1. 明确问题定义
2. 收集相关信息
3. 分析因果关系
4. 制定解决方案
5. 评估和迭代""",
        tags=["问题分析", "方法论", "通用"],
        principles=["系统思维", "根因分析", "迭代改进"]
    )
    print(f"   ✓ 添加通用技能: {general_skill.skill_id}")
    
    # 添加任务特定技能
    print("\n2.2 添加任务特定技能...")
    task_skill = octopai.add_task_specific_skill_to_bank(
        name="代码优化方法",
        description="针对代码性能优化的特定方法",
        content="""# 代码优化方法

## 优化原则
1. 先测量，后优化
2. 优先优化热点代码
3. 保持代码可读性
4. 使用合适的数据结构

## 常见优化技术
- 减少循环内计算
- 使用缓存避免重复计算
- 选择合适的算法复杂度
- 并行化可并行的任务""",
        task_domain="编程",
        tags=["代码优化", "性能", "编程"],
        principles=["性能优先", "可读性平衡", "数据驱动"]
    )
    print(f"   ✓ 添加任务特定技能: {task_skill.skill_id}")
    
    # 添加常见错误
    print("\n2.3 添加常见错误...")
    mistake = octopai.add_common_mistake(
        mistake_id="premature-optimization",
        description="过早优化代码",
        avoid_instruction="先确保功能正确，再进行优化。使用性能分析工具定位瓶颈。",
        related_skill_ids=[task_skill.skill_id],
        tags=["性能", "反模式"]
    )
    print(f"   ✓ 添加常见错误: {mistake.mistake_id}")
    
    # 获取技能注入上下文
    print("\n2.4 生成技能注入上下文...")
    context = octopai.get_skill_injection_context(
        task_context="我需要优化一个数据处理脚本的性能",
        include_general=True,
        include_mistakes=True,
        task_domain="编程",
        max_tokens=3000
    )
    print(f"   ✓ 生成的上下文长度: {len(context)} 字符")
    print("\n上下文预览:")
    print("-" * 70)
    print(context[:500] + "..." if len(context) > 500 else context)
    print("-" * 70)
    
    # ==================== 第2部分：经验提炼 ====================
    print("\n" + "=" * 70)
    print("[3] 经验提炼系统 - ExperienceDistiller")
    print("=" * 70)
    
    trajectory_id = "optimization-task-001"
    
    # 记录成功轨迹
    print("\n3.1 记录成功轨迹...")
    octopai.record_trajectory_step(
        trajectory_id=trajectory_id,
        step_number=1,
        action="分析代码结构，识别关键路径",
        observation="发现循环内有重复计算",
        reasoning="需要先理解代码结构，找到性能瓶颈",
        decision_outcome="identified_bottleneck"
    )
    
    octopai.record_trajectory_step(
        trajectory_id=trajectory_id,
        step_number=2,
        action="使用缓存优化重复计算",
        observation="性能提升了40%",
        reasoning="缓存可以避免重复计算相同的结果",
        decision_outcome="applied_optimization"
    )
    
    octopai.record_trajectory_step(
        trajectory_id=trajectory_id,
        step_number=3,
        action="验证功能正确性",
        observation="所有测试通过",
        reasoning="优化不能破坏原有功能",
        decision_outcome="verified_correctness"
    )
    
    # 完成轨迹
    print("\n3.2 完成轨迹...")
    trajectory = octopai.finalize_trajectory(
        trajectory_id=trajectory_id,
        trajectory_type=TrajectoryType.SUCCESS,
        overall_success=True,
        task_completion="成功优化了数据处理脚本，性能提升40%",
        lessons_learned="缓存优化对重复计算非常有效，但要注意内存使用"
    )
    print(f"   ✓ 轨迹完成: {trajectory.trajectory_id}")
    
    # 提炼成功模式
    print("\n3.3 提炼成功模式...")
    patterns = octopai.distill_success_patterns(
        trajectory_id=trajectory_id,
        min_success_rate=0.7,
        max_patterns=3
    )
    for pattern in patterns:
        print(f"   ✓ 提取模式: {pattern.pattern_name}")
        print(f"     - 置信度: {pattern.confidence_score:.2f}")
        print(f"     - 应用场景: {pattern.application_context[:50]}...")
    
    # ==================== 第3部分：递归进化 ====================
    print("\n" + "=" * 70)
    print("[4] 递归技能进化 - RecursiveEvolution")
    print("=" * 70)
    
    skill_id = "code-optimization-skill"
    
    # 记录技能使用情况
    print("\n4.1 记录技能使用性能...")
    for i in range(15):
        octopai.record_skill_performance_for_evolution(
            skill_id=skill_id,
            version=1,
            success=True if i < 10 else False,
            performance_metrics={"execution_time": 1.5 - i * 0.05},
            context=f"第 {i+1} 次使用"
        )
    print(f"   ✓ 记录了 15 次技能使用")
    
    # 获取性能趋势
    print("\n4.2 查看技能性能趋势...")
    trend = octopai.get_skill_performance_trend(skill_id=skill_id)
    print(f"   - 总使用次数: {trend['total_uses']}")
    print(f"   - 成功率: {trend['success_rate']:.2%}")
    print(f"   - 近期成功率: {trend['recent_success_rate']:.2%}")
    print(f"   - 趋势: {trend['trend']}")
    
    # 触发育进化
    print("\n4.3 触发技能进化...")
    cycle = octopai.trigger_skill_evolution(
        skill_id=skill_id,
        trigger=EvolutionTrigger.PERFORMANCE_DROP,
        current_version=1,
        rationale="近期成功率下降，需要优化技能"
    )
    if cycle:
        print(f"   ✓ 进化周期创建: {cycle.cycle_id}")
        print(f"   - 触发类型: {cycle.trigger.value}")
        print(f"   - 起始版本: {cycle.start_version}")
    
    # 获取进化统计
    print("\n4.4 查看进化引擎统计...")
    stats = octopai.get_evolution_statistics()
    print(f"   - 总周期数: {stats['total_cycles']}")
    print(f"   - 活跃周期: {stats['active_cycles']}")
    print(f"   - 追踪技能数: {stats['skills_tracked']}")
    
    # ==================== 总结 ====================
    print("\n" + "=" * 70)
    print("[5] 示例完成")
    print("=" * 70)
    print("\n本示例展示了 Octopai 的三个核心创新模块：")
    print("\n1. 分层技能库（SkillBank）")
    print("   - 通用技能与任务特定技能分离管理")
    print("   - 常见错误知识库")
    print("   - 智能技能注入上下文生成")
    print("\n2. 经验提炼系统（ExperienceDistiller）")
    print("   - 轨迹记录与分析")
    print("   - 成功模式自动提炼")
    print("   - 失败教训提取")
    print("\n3. 递归技能进化（RecursiveEvolution）")
    print("   - 性能监控与自动触发")
    print("   - 技能版本进化管理")
    print("   - 完整的进化周期追踪")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
