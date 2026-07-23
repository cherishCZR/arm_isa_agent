"""Compile-only verification using local assembler/compiler tools.

This layer deliberately checks only whether generated files compile/assemble.
It does not execute the result.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

from arm_isa_agent.verification.models import CompileResult, CompileSummary

FEATURE_TO_CLANG_EXTENSION = {
    "FEAT_SVE": "sve",
    "FEAT_SVE2": "sve2",
    "FEAT_SME": "sme",
    "FEAT_MOPS": "mops",
    "FEAT_LS64": "ls64",
    "FEAT_CSSC": "cssc",
}


class CompileVerifier:
    """Run compile-only verification for generated test files."""

    def __init__(
        self,
        asm_tool: str | None = None,
        c_compiler: str | None = None,
        target: str | None = None,
        timeout_sec: int | None = None,
    ) -> None:
        self.asm_tool = asm_tool or os.getenv("ARM_ASM_TOOLCHAIN", "llvm-mc")
        self.c_compiler = c_compiler or os.getenv("ARM_C_COMPILER", "clang")
        self.target = target or os.getenv("ARM_TARGET", "aarch64")
        self.timeout_sec = int(timeout_sec or os.getenv("COMPILE_TIMEOUT_SEC", "10"))

    def verify_files(self, test_files: list[dict[str, Any]]) -> CompileSummary:
        results = [self.verify_file(tf) for tf in test_files]
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        skipped = sum(1 for r in results if r.status == "SKIPPED")
        if failed:
            status = "FAIL"
        elif passed and not failed:
            status = "PASS"
        else:
            status = "SKIPPED"
        return CompileSummary(
            status=status,
            total=len(results),
            passed=passed,
            failed=failed,
            skipped=skipped,
            results=results,
        )

    def verify_file(self, test_file: dict[str, Any]) -> CompileResult:
        fmt = (test_file.get("format") or "").lower()
        if fmt in {"s", "llvm"}:
            return self._verify_asm(test_file)
        if fmt in {"c", "cpp"}:
            return self._verify_c_like(test_file)
        return CompileResult(
            file_id=test_file.get("file_id", ""),
            filename=test_file.get("filename", ""),
            status="SKIPPED",
            reason=f"Unsupported file format for compile verification: {fmt or '<empty>'}",
        )

    def _verify_asm(self, test_file: dict[str, Any]) -> CompileResult:
        tool_path = self._which(self.asm_tool)
        if tool_path is not None and Path(tool_path).name.lower().startswith("llvm-mc"):
            mattr = self._mattr_args(test_file)
            command = [tool_path, "-triple", self.target, *mattr, "-filetype=obj"]
            return self._run_with_temp_file(test_file, command, suffix=".S")

        clang_path = self._which(self.c_compiler)
        if clang_path is not None:
            command = [clang_path, "--target=aarch64-linux-gnu", "-c", "-x", "assembler"]
            march = self._clang_march_arg(test_file)
            if march:
                command.append(march)
            return self._run_with_temp_file(test_file, command, suffix=".S")

        if tool_path is None:
            return CompileResult(
                file_id=test_file.get("file_id", ""),
                filename=test_file.get("filename", ""),
                status="SKIPPED",
                toolchain=f"{self.asm_tool}/{self.c_compiler}",
                reason=f"Neither {self.asm_tool} nor {self.c_compiler} was found",
            )

        return CompileResult(
            file_id=test_file.get("file_id", ""),
            filename=test_file.get("filename", ""),
            status="SKIPPED",
            toolchain=self.asm_tool,
            reason=f"{self.asm_tool} is not supported as an assembler tool in this verifier",
        )

    def _verify_c_like(self, test_file: dict[str, Any]) -> CompileResult:
        tool_path = self._which(self.c_compiler)
        if tool_path is None:
            return CompileResult(
                file_id=test_file.get("file_id", ""),
                filename=test_file.get("filename", ""),
                status="SKIPPED",
                toolchain=self.c_compiler,
                reason=f"{self.c_compiler} not found on PATH",
            )

        suffix = ".cpp" if (test_file.get("format") or "").lower() == "cpp" else ".c"
        command = [tool_path, "--target=aarch64-linux-gnu", "-c"]
        march = self._clang_march_arg(test_file)
        if march:
            command.append(march)
        return self._run_with_temp_file(test_file, command, suffix=suffix)

    @staticmethod
    def _which(tool: str) -> str | None:
        found = shutil.which(tool)
        if found:
            return found

        candidates = [
            Path("C:/Program Files/LLVM/bin") / tool,
            Path("C:/Program Files/LLVM/bin") / f"{tool}.exe",
            Path.home() / "AppData/Local/Programs/LLVM/bin" / tool,
            Path.home() / "AppData/Local/Programs/LLVM/bin" / f"{tool}.exe",
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
        return None

    def _run_with_temp_file(self, test_file: dict[str, Any], command_prefix: list[str], suffix: str) -> CompileResult:
        content = test_file.get("content", "")
        started = time.perf_counter()
        with tempfile.TemporaryDirectory(prefix="arm_isa_compile_") as td:
            src = Path(td) / f"input{suffix}"
            out = Path(td) / "out.o"
            src.write_text(content, encoding="utf-8")
            command = [*command_prefix, str(src), "-o", str(out)]
            try:
                proc = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_sec,
                    check=False,
                )
                status = "PASS" if proc.returncode == 0 else "FAIL"
                return CompileResult(
                    file_id=test_file.get("file_id", ""),
                    filename=test_file.get("filename", ""),
                    status=status,
                    toolchain=Path(command[0]).name,
                    command=command,
                    return_code=proc.returncode,
                    stdout=proc.stdout[-4000:],
                    stderr=proc.stderr[-4000:],
                    duration_ms=(time.perf_counter() - started) * 1000,
                )
            except subprocess.TimeoutExpired as exc:
                return CompileResult(
                    file_id=test_file.get("file_id", ""),
                    filename=test_file.get("filename", ""),
                    status="FAIL",
                    toolchain=Path(command[0]).name,
                    command=command,
                    stdout=(exc.stdout or "")[-4000:] if isinstance(exc.stdout, str) else "",
                    stderr=(exc.stderr or "")[-4000:] if isinstance(exc.stderr, str) else "",
                    duration_ms=(time.perf_counter() - started) * 1000,
                    reason=f"Compile timed out after {self.timeout_sec}s",
                )

    @staticmethod
    def _mattr_args(test_file: dict[str, Any]) -> list[str]:
        flags = [f"+{extension}" for extension in CompileVerifier._required_extensions(test_file)]
        return ["-mattr=" + ",".join(flags)] if flags else []

    @staticmethod
    def _clang_march_arg(test_file: dict[str, Any]) -> str | None:
        extensions = CompileVerifier._required_extensions(test_file)
        return "-march=armv9-a+" + "+".join(extensions) if extensions else None

    @staticmethod
    def _required_extensions(test_file: dict[str, Any]) -> list[str]:
        """Derive compiler extensions from XML profile metadata, not asm text."""
        explicit_features = test_file.get("required_features")
        extensions: list[str] = []
        if isinstance(explicit_features, list):
            for feature in explicit_features:
                extension = FEATURE_TO_CLANG_EXTENSION.get(str(feature).upper())
                if extension and extension not in extensions:
                    extensions.append(extension)
        if extensions:
            return extensions

        # Compatibility fallback for legacy test files without profile metadata.
        text = " ".join([
            str(test_file.get("description", "")),
            str(test_file.get("content", ""))[:1000],
        ]).lower()
        for token, ext in [
            ("sve2", "sve2"),
            ("sve", "sve"),
            ("sme", "sme"),
            ("mops", "mops"),
            ("ls64", "ls64"),
            ("cssc", "cssc"),
        ]:
            if token in text and ext not in extensions:
                extensions.append(ext)
        return extensions
