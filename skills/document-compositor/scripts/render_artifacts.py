#!/usr/bin/env python3
"""Render application artifacts and emit hash-bound page evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_assignment(value: str, label: str) -> tuple[str, str]:
    if "=" not in value:
        raise argparse.ArgumentTypeError(f"{label} must use ID=VALUE")
    identifier, raw = value.split("=", 1)
    if not identifier.strip() or not raw.strip():
        raise argparse.ArgumentTypeError(f"{label} requires a non-empty ID and value")
    return identifier.strip(), raw.strip()


def capability_report(args: argparse.Namespace) -> dict[str, object]:
    renderer = Path(args.docx_renderer).expanduser().resolve() if args.docx_renderer else None
    raw_pdftoppm = args.pdftoppm or shutil.which("pdftoppm")
    pdftoppm = Path(raw_pdftoppm).expanduser().resolve() if raw_pdftoppm else None
    return {
        "schema_version": "1.0",
        "docx_renderer": {
            "available": bool(renderer and renderer.is_file()),
            "path": str(renderer) if renderer else None,
            "sha256": sha256_file(renderer) if renderer and renderer.is_file() else None,
        },
        "pdftoppm": {
            "available": bool(pdftoppm and pdftoppm.is_file()),
            "path": str(pdftoppm) if pdftoppm else None,
            "sha256": sha256_file(pdftoppm) if pdftoppm and pdftoppm.is_file() else None,
        },
        "python": {
            "path": str(Path(sys.executable).absolute()),
            "sha256": sha256_file(Path(sys.executable).absolute()),
        },
    }


def page_records(directory: Path) -> list[dict[str, object]]:
    pages = sorted(directory.glob("page-*.png"), key=lambda path: int(path.stem.split("-")[-1]))
    if not pages:
        pages = sorted(directory.glob("*.png"))
    if not pages:
        raise RuntimeError(f"Renderer produced no PNG pages in {directory}")
    return [
        {
            "page": index,
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for index, path in enumerate(pages, start=1)
    ]


def render_pdf(source: Path, destination: Path, pdftoppm: str) -> list[dict[str, object]]:
    destination.mkdir(parents=True, exist_ok=True)
    prefix = destination / "page"
    subprocess.run([pdftoppm, "-png", str(source), str(prefix)], check=True)
    generated = sorted(destination.glob("page-*.png"))
    for index, path in enumerate(generated, start=1):
        target = destination / f"page-{index}.png"
        if path != target:
            path.rename(target)
    return page_records(destination)


def render_docx(source: Path, destination: Path, renderer: Path) -> list[dict[str, object]]:
    destination.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [sys.executable, str(renderer), str(source), "--output_dir", str(destination), "--emit_pdf"],
        check=True,
    )
    return page_records(destination)


def render(args: argparse.Namespace) -> int:
    assignments = [parse_assignment(value, "--artifact") for value in args.artifact]
    expected = {key: int(value) for key, value in (parse_assignment(item, "--expected-pages") for item in args.expected_pages)}
    if len({key for key, _ in assignments}) != len(assignments):
        raise SystemExit("Artifact identifiers must be unique")

    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    raw_pdftoppm = args.pdftoppm or shutil.which("pdftoppm")
    pdftoppm = str(Path(raw_pdftoppm).expanduser().resolve()) if raw_pdftoppm else None
    renderer = Path(args.docx_renderer).expanduser().resolve() if args.docx_renderer else None
    records: list[dict[str, object]] = []

    for identifier, raw_path in assignments:
        source = Path(raw_path).expanduser().resolve()
        if not source.is_file():
            raise SystemExit(f"Missing artifact {identifier}: {source}")
        destination = output / identifier
        suffix = source.suffix.lower()
        if suffix == ".pdf":
            if not pdftoppm:
                raise SystemExit("pdftoppm is required to render PDF artifacts")
            pages = render_pdf(source, destination, pdftoppm)
        elif suffix == ".docx":
            if not renderer or not renderer.is_file():
                raise SystemExit("--docx-renderer must point to the host's verified render_docx.py")
            pages = render_docx(source, destination, renderer)
        else:
            raise SystemExit(f"Unsupported artifact format for {source}")
        if identifier in expected and len(pages) != expected[identifier]:
            raise SystemExit(f"{identifier} rendered {len(pages)} pages; expected {expected[identifier]}")
        records.append(
            {
                "id": identifier,
                "source": str(source),
                "format": suffix[1:],
                "sha256": sha256_file(source),
                "bytes": source.stat().st_size,
                "pages": pages,
            }
        )

    manifest = {
        "schema_version": "1.0",
        "tool_capabilities": capability_report(args),
        "artifacts": records,
    }
    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(manifest_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    capabilities = subparsers.add_parser("capabilities", help="Report renderer availability")
    capabilities.add_argument("--docx-renderer")
    capabilities.add_argument("--pdftoppm")

    render_parser = subparsers.add_parser("render", help="Render artifacts and record page hashes")
    render_parser.add_argument("--artifact", action="append", required=True, metavar="ID=PATH")
    render_parser.add_argument("--expected-pages", action="append", default=[], metavar="ID=COUNT")
    render_parser.add_argument("--output-dir", required=True)
    render_parser.add_argument("--manifest", required=True)
    render_parser.add_argument("--docx-renderer")
    render_parser.add_argument("--pdftoppm")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "capabilities":
        print(json.dumps(capability_report(args), indent=2, sort_keys=True))
        return 0
    return render(args)


if __name__ == "__main__":
    raise SystemExit(main())
