"""ARM ISA Agent Tools — retrieval, query, generation, planning, testgen, review, and self-correction capabilities."""

from arm_isa_agent.tools.retrieval import (
    query_constraint,
    query_encoding,
    query_instruction,
    retrieve_instruction,
)
from arm_isa_agent.tools.generation import (
    generate_assembly,
    generate_inline_asm,
    generate_testcase,
    validate_operand,
)
from arm_isa_agent.tools.planning import analyze_instruction_profile, plan_instruction_tests
from arm_isa_agent.tools.review import review_result
from arm_isa_agent.tools.testgen import (
    generate_alias_tests,
    generate_asm_tests,
    generate_boundary_tests,
    generate_feature_enable_tests,
    generate_inline_asm_tests,
    generate_invalid_operand_tests,
    generate_llvm_mc_tests,
    generate_test_suite,
)
from arm_isa_agent.tools.review_gen import (
    repair_testcase,
    review_test_suite,
    review_testcase,
)

# Import to trigger @register_tool side effects
__all__ = [
    "retrieve_instruction",
    "query_instruction",
    "query_encoding",
    "query_constraint",
    "validate_operand",
    "generate_assembly",
    "generate_inline_asm",
    "generate_testcase",
    "plan_instruction_tests",
    "analyze_instruction_profile",
    "review_result",
    "generate_test_suite",
    "generate_asm_tests",
    "generate_llvm_mc_tests",
    "generate_inline_asm_tests",
    "generate_boundary_tests",
    "generate_alias_tests",
    "generate_invalid_operand_tests",
    "generate_feature_enable_tests",
    "review_testcase",
    "review_test_suite",
    "repair_testcase",
]
