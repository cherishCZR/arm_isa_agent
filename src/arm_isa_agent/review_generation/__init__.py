"""Testcase Reviewer Agent — 5-dimension automated review + self-correction repair loop.

Review dimensions:
- Syntax Review  (ARM asm / LLVM MC / C++ 语法正确性)
- Constraint Review  (操作数约束合规检查)
- Encoding Review  (编码位域对应检查)
- Semantic Review  (语义/参考模型验证)
- Coverage Review  (TestPlan 覆盖率比对)

Workflow:   Planner → Generator → Reviewer → Decision
                                   ↑              ↓
                                   └── Repair ←───┘  (max 3 loops)
"""

from arm_isa_agent.review_generation.models import (
    DimensionScore,
    RepairResult,
    ReviewIssue,
    ReviewResult,
)
from arm_isa_agent.review_generation.reviewer import (
    ConstraintReviewer,
    CoverageReviewer,
    EncodingReviewer,
    RepairGenerator,
    SemanticReviewer,
    SyntaxReviewer,
    TestcaseReviewer,
)

__all__ = [
    # Models
    "ReviewIssue",
    "ReviewResult",
    "DimensionScore",
    "RepairResult",
    # 5 Reviewers
    "SyntaxReviewer",
    "ConstraintReviewer",
    "EncodingReviewer",
    "SemanticReviewer",
    "CoverageReviewer",
    # Orchestrator + Repair
    "TestcaseReviewer",
    "RepairGenerator",
]
