from __future__ import annotations


class ArmISAAgentError(Exception):
    """ARM ISA Agent 基础异常."""

    def __init__(self, message: str, *args: object) -> None:
        super().__init__(message, *args)
        self.message = message


class ParseError(ArmISAAgentError):
    """XML 解析错误."""


class KBError(ArmISAAgentError):
    """知识库操作错误."""


class AgentError(ArmISAAgentError):
    """Agent 运行时错误."""


class ConfigError(ArmISAAgentError):
    """配置错误."""


class ETLPipelineError(ArmISAAgentError):
    """ETL 管道错误."""


class ValidationError(ArmISAAgentError):
    """数据校验错误."""
