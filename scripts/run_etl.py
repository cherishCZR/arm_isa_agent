"""快速 ETL 运行脚本."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from arm_isa_agent.etl.pipeline import ETLPipeline

pipeline = ETLPipeline()
stats = pipeline.run_full(truncate=True, no_cards=False)
