from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .contracts import ContractError
from .engine import capability_report, run_manifest, validate_run


def _emit(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="application-pack",
        description="Build and release a hash-bound, evidence-backed application package.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run or resume a package from a manifest")
    run_parser.add_argument("manifest", type=Path, help="Path to run-manifest.json")

    validate_parser = subparsers.add_parser("validate", help="Revalidate an existing run")
    validate_parser.add_argument("run_dir", type=Path, help="Run directory containing work/ and audit/")

    capabilities_parser = subparsers.add_parser("capabilities", help="Describe required host capabilities")
    capabilities_parser.add_argument("--profile", type=Path, help="Optional profile.json or profile directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "run":
            code, result = run_manifest(args.manifest)
            _emit(result)
            return code
        if args.command == "validate":
            result = validate_run(args.run_dir)
            _emit(result)
            return 0 if result["status"] == "pass" else 2
        if args.command == "capabilities":
            _emit(capability_report(args.profile))
            return 0
    except (ContractError, FileNotFoundError, json.JSONDecodeError, OSError, ValueError) as exc:
        _emit({"status": "error", "error": str(exc)})
        return 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
