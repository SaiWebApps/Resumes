#!/usr/bin/env python3
"""Install or package the canonical Agent Skills for supported hosts."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import time
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
SKILL_NAMES = (
    "application-package",
    "career-evidence",
    "opportunity-auditor",
    "application-positioner",
    "resume-author",
    "speaker-pitch-author",
    "document-compositor",
    "artifact-change-controller",
    "submission-release-auditor",
)

RUNTIME_PATHS = (
    "pyproject.toml",
    "README.md",
    "src",
    "schemas",
    "bin",
)


def validate_sources() -> None:
    missing = [name for name in SKILL_NAMES if not (SKILLS_ROOT / name / "SKILL.md").is_file()]
    if missing:
        raise SystemExit(f"Missing canonical skills: {', '.join(missing)}")


def preserve_existing(path: Path, force: bool) -> None:
    if not path.exists() and not path.is_symlink():
        return
    if not force:
        raise SystemExit(f"Target exists: {path}. Re-run with --force to preserve it in a backup.")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_root = path.parent / ".application-pack-backups" / stamp
    backup_root.mkdir(parents=True, exist_ok=True)
    path.rename(backup_root / path.name)


def install_directory(target_home: Path, mode: str, force: bool) -> None:
    target_home.mkdir(parents=True, exist_ok=True)
    for name in SKILL_NAMES:
        source = (SKILLS_ROOT / name).resolve()
        target = target_home / name
        if target.is_symlink() and target.resolve() == source and mode == "symlink":
            print(f"current {target}")
            continue
        preserve_existing(target, force)
        if mode == "symlink":
            target.symlink_to(source, target_is_directory=True)
        else:
            shutil.copytree(source, target)
        print(f"installed {target}")


def package_chatgpt(output: Path, force: bool) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for name in SKILL_NAMES:
        archive = output / f"{name}.skill"
        preserve_existing(archive, force)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
            source = SKILLS_ROOT / name
            for path in sorted(source.rglob("*")):
                if path.is_file():
                    bundle.write(path, Path(name) / path.relative_to(source))
            if name == "application-package":
                for relative in RUNTIME_PATHS:
                    source_path = ROOT / relative
                    paths = source_path.rglob("*") if source_path.is_dir() else (source_path,)
                    for path in sorted(paths):
                        if path.is_file() and "__pycache__" not in path.parts:
                            bundle.write(path, Path(name) / "runtime" / path.relative_to(ROOT))
        print(f"packaged {archive}")


def package_generic(output: Path, force: bool) -> None:
    preserve_existing(output, force)
    output.mkdir(parents=True)
    shutil.copytree(SKILLS_ROOT, output / "skills")
    shutil.copy2(ROOT / "adapters" / "generic" / "BOOTSTRAP.md", output / "BOOTSTRAP.md")
    for relative in RUNTIME_PATHS:
        source = ROOT / relative
        destination = output / relative
        if source.is_dir():
            shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
    print(f"packaged {output}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=("codex", "claude", "chatgpt", "generic", "all"), required=True)
    parser.add_argument("--mode", choices=("symlink", "copy"), default="symlink")
    parser.add_argument("--destination", type=Path, help="Override the selected target's default directory")
    parser.add_argument("--force", action="store_true", help="Move an existing target into a timestamped backup")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validate_sources()
    selected = ("codex", "claude", "chatgpt", "generic") if args.target == "all" else (args.target,)
    if args.destination and len(selected) > 1:
        raise SystemExit("--destination may be used only with one target")
    for target in selected:
        if target == "codex":
            install_directory(args.destination or Path("~/.codex/skills").expanduser(), args.mode, args.force)
        elif target == "claude":
            # Claude Code supports isolated configuration roots through
            # CLAUDE_CONFIG_DIR.  Honor that boundary instead of writing to
            # the legacy ~/.claude location, which may intentionally be an
            # immutable sentinel.
            config_root = Path(os.environ.get("CLAUDE_CONFIG_DIR", "~/.claude")).expanduser()
            install_directory(args.destination or config_root / "skills", args.mode, args.force)
        elif target == "chatgpt":
            package_chatgpt(args.destination or ROOT / "dist" / "chatgpt", args.force)
        else:
            package_generic(args.destination or ROOT / "dist" / "generic", args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
