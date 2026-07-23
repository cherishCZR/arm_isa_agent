from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, ClassVar

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict


# ── LLM Presets ────────────────────────────────────────────────
# Provide convenient aliases for common model setups.
#           model           base_url                            api_key (placeholder if not needed)
LLM_PRESETS: dict[str, dict[str, str]] = {
    "local": {
        "llm_model": "qwen3:8b",
        "llm_base_url": "http://localhost:11434/v1",
        "llm_api_key": "ollama",  # Ollama doesn't require a real key
        "llm_provider": "ollama",
    },
    "deepseek": {
        "llm_model": "deepseek-chat",
        "llm_base_url": "https://api.deepseek.com/v1",
        "llm_api_key": "",  # set via env / CLI
        "llm_provider": "deepseek",
    },
}


class Settings(BaseSettings):
    """全局配置，可通过环境变量或 .env 文件覆盖."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix="ARM_ISA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ---- 下划线路径 ----
    data_dir: Path = Path("data")
    raw_xml_dir: Path = Path("ISA_A64_xml_A_profile-2025-03/ISA_A64_xml_A_profile-2025-03")

    # ---- SQLite ----
    sqlite_db_path: Path = Path("data/sqlite/isa_kb.db")

    # ---- ChromaDB ----
    chroma_persist_dir: Path = Path("data/chroma")
    chroma_collection_name: str = "instruction_cards"

    # ---- BM25 ----
    bm25_cache_dir: Path = Path("data/bm25")

    # ---- Embedding ----
    embedding_model_name: str = "BAAI/bge-m3"
    embedding_device: str = "cpu"
    embedding_batch_size: int = 32

    # ---- LLM ----
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_api_key: str = ""
    llm_base_url: str = ""
    llm_temperature: float = 0.0

    # ---- LLM Preset ----
    llm_preset: str = ""  # "local" | "deepseek" | "" (manual config)

    # ---- ETL ----
    etl_batch_size: int = 100
    etl_max_workers: int = 4
    etl_skip_invalid: bool = True

    # ---- API ----
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1

    # ---- Logging ----
    log_level: str = "INFO"
    log_format: str = "json"  # json | console

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Store explicitly-provided field names (bypass pydantic validation)
        self.__dict__["_explicit_fields"] = set(kwargs.keys())
        # Auto-apply LLM preset if specified
        self._apply_preset()
        # 确保路径为绝对路径
        if not self.data_dir.is_absolute():
            self.data_dir = Path.cwd() / self.data_dir
        if not self.raw_xml_dir.is_absolute():
            self.raw_xml_dir = Path.cwd() / self.raw_xml_dir
        if not self.sqlite_db_path.is_absolute():
            self.sqlite_db_path = self.data_dir / "sqlite" / "isa_kb.db"
        if not self.chroma_persist_dir.is_absolute():
            self.chroma_persist_dir = self.data_dir / "chroma"

    def _apply_preset(self) -> None:
        """Apply LLM preset values; explicit kwargs/env overrides take precedence."""
        preset_name = self.llm_preset.strip().lower()
        if not preset_name or preset_name not in LLM_PRESETS:
            return
        preset = LLM_PRESETS[preset_name]
        explicit = self.__dict__.get("_explicit_fields", set())
        for key, preset_val in preset.items():
            # Fields explicitly passed via kwargs override the preset
            if key in explicit:
                continue
            # For llm_api_key: if env already set a non-empty value, keep it
            current = getattr(self, key, None)
            if current and key == "llm_api_key":
                continue
            setattr(self, key, preset_val)


def setup_logging(settings: Settings) -> None:
    """配置结构化日志."""
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    if settings.log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            timestamper,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # 设置标准库日志级别
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )


# 全局单例
_settings: Settings | None = None


def get_settings() -> Settings:
    """获取全局配置单例."""
    global _settings
    if _settings is None:
        _settings = Settings()
        setup_logging(_settings)
    return _settings
