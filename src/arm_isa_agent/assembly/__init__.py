"""XML-template based assembly generation."""

from arm_isa_agent.assembly.instantiator import AssemblyInstantiator
from arm_isa_agent.assembly.scenario import ScenarioProgramGenerator, parse_scenario_text
from arm_isa_agent.assembly.single_suite import SingleInstructionSuiteGenerator

__all__ = ["AssemblyInstantiator", "ScenarioProgramGenerator", "SingleInstructionSuiteGenerator", "parse_scenario_text"]
