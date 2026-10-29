from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Any

from .artifacts import sha256_file
from .contracts import ContractError


def _renderer_path(
    capabilities: dict[str, Any],
    key: str,
    *,
    executable: bool,
    preserve_symlink: bool = False,
) -> Path:
    entry = capabilities.get(key)
    if not isinstance(entry, dict):
        raise ContractError(f"Render evidence lacks {key} renderer identity")
    raw_path = entry.get("path")
    expected_hash = entry.get("sha256")
    if not isinstance(raw_path, str) or not raw_path:
        raise ContractError(f"Render evidence lacks {key} renderer path")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ContractError(f"Render evidence lacks {key} renderer SHA-256")
    path = Path(raw_path).expanduser().absolute()
    if not preserve_symlink:
        path = path.resolve()
    if not path.is_file():
        raise ContractError(f"Declared {key} renderer is unavailable: {path}")
    if executable and not path.stat().st_mode & 0o111:
        raise ContractError(f"Declared {key} renderer is not executable: {path}")
    actual_hash = sha256_file(path)
    if actual_hash != expected_hash:
        raise ContractError(f"Declared {key} renderer identity changed")
    return path


def verified_renderer_identities(capabilities: dict[str, Any]) -> dict[str, dict[str, str]]:
    pdftoppm = _renderer_path(capabilities, "pdftoppm", executable=True)
    docx_renderer = _renderer_path(capabilities, "docx_renderer", executable=False)
    python = _renderer_path(capabilities, "python", executable=True, preserve_symlink=True)
    return {
        "pdftoppm": {"path": str(pdftoppm), "sha256": sha256_file(pdftoppm)},
        "docx_renderer": {"path": str(docx_renderer), "sha256": sha256_file(docx_renderer)},
        "python": {"path": str(python), "sha256": sha256_file(python)},
    }


def _page_files(directory: Path) -> list[Path]:
    pages = sorted(directory.glob("page-*.png"), key=lambda path: int(path.stem.split("-")[-1]))
    if not pages:
        pages = sorted(directory.glob("*.png"))
    if not pages:
        raise ContractError(f"Renderer produced no PNG pages in {directory}")
    return pages


def render_exact_artifact(
    source: Path,
    artifact_format: str,
    capabilities: dict[str, Any],
    output_dir: Path,
) -> list[Path]:
    """Regenerate pages from candidate bytes with the declared renderer.

    The renderer executables are hash-identified before invocation.  Commands
    are passed as argument arrays, never through a shell.
    """

    identities = verified_renderer_identities(capabilities)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    try:
        if artifact_format == "pdf":
            prefix = output_dir / "page"
            command = [identities["pdftoppm"]["path"], "-png", str(source), str(prefix)]
        elif artifact_format == "docx":
            command = [
                identities["python"]["path"],
                identities["docx_renderer"]["path"],
                str(source),
                "--output_dir",
                str(output_dir),
                "--emit_pdf",
            ]
        else:
            raise ContractError(f"Unsupported render format {artifact_format!r}")
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=180)
    except (OSError, subprocess.SubprocessError) as exc:
        detail = getattr(exc, "stderr", None) or str(exc)
        raise ContractError(f"Fresh {artifact_format} render failed for {source.name}: {detail.strip()}") from exc
    return _page_files(output_dir)


def require_fresh_render_match(
    source: Path,
    artifact_id: str,
    artifact_format: str,
    supplied_pages: list[dict[str, Any]],
    capabilities: dict[str, Any],
    output_dir: Path,
) -> None:
    fresh_pages = render_exact_artifact(source, artifact_format, capabilities, output_dir)
    if len(fresh_pages) != len(supplied_pages):
        raise ContractError(
            f"Render evidence for {artifact_id} does not match a fresh render: "
            f"supplied {len(supplied_pages)} pages, regenerated {len(fresh_pages)}"
        )
    for page_number, (fresh, supplied) in enumerate(zip(fresh_pages, supplied_pages), start=1):
        fresh_hash = sha256_file(fresh)
        if fresh_hash != supplied.get("sha256") or fresh.stat().st_size != supplied.get("bytes"):
            raise ContractError(
                f"Render evidence for {artifact_id} page {page_number} does not match a fresh render"
            )
