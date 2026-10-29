from __future__ import annotations

import hashlib
from io import BytesIO
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
WORD_NS = WORD_NAMESPACE["w"]
WORD_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
WORD_DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
CORE_NS = "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
DC_NS = "http://purl.org/dc/elements/1.1/"
DCTERMS_NS = "http://purl.org/dc/terms/"
APP_NS = "http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"


def _word_attr(name: str) -> str:
    return f"{{{WORD_NS}}}{name}"


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as stream:
        return json.load(stream)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def normalize_semantic_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u00ad", "").replace("\u200b", "")
    return " ".join(re.findall(r"[^\W_]+", text.casefold(), flags=re.UNICODE))


def extract_docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as package:
            document = ElementTree.fromstring(package.read("word/document.xml"))
    except (KeyError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        raise ValueError(f"Unreadable DOCX {path}: {exc}") from exc

    paragraphs: list[str] = []
    for paragraph in document.findall(".//w:p", WORD_NAMESPACE):
        fragments: list[str] = []
        for node in paragraph.iter():
            local_name = node.tag.rsplit("}", 1)[-1]
            if local_name == "t":
                fragments.append(node.text or "")
            elif local_name == "tab":
                fragments.append("\t")
            elif local_name in {"br", "cr"}:
                fragments.append("\n")
        if fragments:
            paragraphs.append("".join(fragments))
    return "\n".join(paragraphs)


def _xml_text(root: ElementTree.Element, namespace: str, name: str) -> str:
    node = root.find(f"{{{namespace}}}{name}")
    return (node.text or "").strip() if node is not None else ""


def docx_visual_findings(path: Path, expected_pages: int | None = None) -> list[str]:
    """Return deterministic findings for text hidden by Word run formatting.

    Render review remains mandatory, but a reviewer attestation must not be able
    to bless text that is structurally invisible.  This intentionally targets
    objective failures (hidden/vanished runs and white body text), not design
    taste.  It also rejects implausibly large body runs that can preserve text
    extraction while destroying pagination.
    """

    try:
        with zipfile.ZipFile(path) as package:
            names = set(package.namelist())
            thumbnail = (
                package.read("docProps/thumbnail.jpeg")
                if "docProps/thumbnail.jpeg" in names
                else None
            )
            document = ElementTree.fromstring(package.read("word/document.xml"))
            settings = ElementTree.fromstring(package.read("word/settings.xml"))
            core = ElementTree.fromstring(package.read("docProps/core.xml"))
            app = ElementTree.fromstring(package.read("docProps/app.xml"))
    except (KeyError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        return [f"Unreadable DOCX {path.name}: {exc}"]

    findings: list[str] = []
    if thumbnail is not None:
        try:
            with Image.open(BytesIO(thumbnail)) as preview:
                extrema = preview.convert("RGB").getextrema()
            if all(high - low <= 2 for low, high in extrema):
                findings.append("DOCX contains a blank template thumbnail instead of a current preview")
        except (OSError, UnidentifiedImageError):
            findings.append("DOCX thumbnail is unreadable")
    save_preview = settings.find("w:savePreviewPicture", WORD_NAMESPACE)
    save_preview_value = (
        save_preview.get(_word_attr("val"), "true").casefold()
        if save_preview is not None
        else "false"
    )
    if save_preview is not None and save_preview_value not in {"0", "false", "off", "no"}:
        findings.append("DOCX requests savePreviewPicture despite having no verified current preview")

    core_fields = {
        "title": _xml_text(core, DC_NS, "title"),
        "subject": _xml_text(core, DC_NS, "subject"),
        "creator": _xml_text(core, DC_NS, "creator"),
        "description": _xml_text(core, DC_NS, "description"),
        "lastModifiedBy": _xml_text(core, CORE_NS, "lastModifiedBy"),
        "created": _xml_text(core, DCTERMS_NS, "created"),
        "modified": _xml_text(core, DCTERMS_NS, "modified"),
    }
    for field, value in core_fields.items():
        if not value:
            findings.append(f"DOCX core metadata field {field} is empty")
    if "python-docx" in core_fields["description"].casefold():
        findings.append("DOCX retains the default generated by python-docx description")
    stale_timestamp = "2013-12-23T23:15:00Z"
    if core_fields["created"] == stale_timestamp or core_fields["modified"] == stale_timestamp:
        findings.append("DOCX retains python-docx template timestamps from 2013")

    app_counts: dict[str, int | None] = {}
    for name in ("Pages", "Words", "Characters", "CharactersWithSpaces"):
        raw_value = _xml_text(app, APP_NS, name)
        try:
            app_counts[name] = int(raw_value)
        except ValueError:
            app_counts[name] = None
        if app_counts[name] is None or app_counts[name] <= 0:
            findings.append(f"DOCX app metadata {name} must be a positive current count")
    if expected_pages is not None and app_counts.get("Pages") != expected_pages:
        findings.append(
            f"DOCX app metadata reports {app_counts.get('Pages')} pages; expected {expected_pages}"
        )

    for index, run in enumerate(document.findall(".//w:r", WORD_NAMESPACE), start=1):
        text = "".join(node.text or "" for node in run.findall(".//w:t", WORD_NAMESPACE)).strip()
        if not text:
            continue
        properties = run.find("w:rPr", WORD_NAMESPACE)
        if properties is None:
            continue
        if properties.find("w:vanish", WORD_NAMESPACE) is not None or properties.find("w:webHidden", WORD_NAMESPACE) is not None:
            findings.append(f"Run {index} is hidden but contains text")
        color = properties.find("w:color", WORD_NAMESPACE)
        color_value = (color.get(_word_attr("val"), "") if color is not None else "").upper().lstrip("#")
        if color_value in {"FFFFFF", "FFF"}:
            findings.append(f"Run {index} uses white text that is invisible on the document background")
        size = properties.find("w:sz", WORD_NAMESPACE)
        size_value = size.get(_word_attr("val")) if size is not None else None
        try:
            point_size = float(size_value) / 2 if size_value is not None else None
        except ValueError:
            point_size = None
        if point_size is not None and point_size > 54:
            findings.append(f"Run {index} uses implausible {point_size:g} pt text")
    return findings


def extract_pdf_text(path: Path) -> tuple[str, int]:
    try:
        reader = PdfReader(str(path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise ValueError(f"Unreadable PDF {path}: {exc}") from exc
    return text, len(reader.pages)


def _valid_external_target(value: str) -> bool:
    return value.startswith(("https://", "http://", "mailto:", "tel:"))


def _docx_style_bold(
    style_id: str | None,
    styles: dict[str, ElementTree.Element],
) -> bool:
    visited: set[str] = set()
    while style_id and style_id not in visited:
        visited.add(style_id)
        style = styles.get(style_id)
        if style is None:
            break
        properties = style.find("w:rPr", WORD_NAMESPACE)
        bold = properties.find("w:b", WORD_NAMESPACE) if properties is not None else None
        if bold is not None:
            return bold.get(_word_attr("val"), "true").casefold() not in {"0", "false", "off", "no"}
        based_on = style.find("w:basedOn", WORD_NAMESPACE)
        style_id = based_on.get(_word_attr("val")) if based_on is not None else None
    return False


def _docx_semantic_metadata(path: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    try:
        with zipfile.ZipFile(path) as package:
            document = ElementTree.fromstring(package.read("word/document.xml"))
            relationships = ElementTree.fromstring(package.read("word/_rels/document.xml.rels"))
            styles_root = ElementTree.fromstring(package.read("word/styles.xml"))
            core = ElementTree.fromstring(package.read("docProps/core.xml"))
    except (KeyError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        raise ValueError(f"Unreadable DOCX {path}: {exc}") from exc

    links = sorted({
        str(relationship.get("Target"))
        for relationship in relationships.findall(f"{{{WORD_REL_NS}}}Relationship")
        if relationship.get("TargetMode") == "External"
        and str(relationship.get("Type", "")).endswith("/hyperlink")
        and relationship.get("Target")
    })
    styles = {
        str(style.get(_word_attr("styleId"))): style
        for style in styles_root.findall("w:style", WORD_NAMESPACE)
        if style.get(_word_attr("styleId"))
    }
    emphasized_tokens: list[str] = []
    for paragraph in document.findall(".//w:p", WORD_NAMESPACE):
        paragraph_properties = paragraph.find("w:pPr", WORD_NAMESPACE)
        paragraph_style = (
            paragraph_properties.find("w:pStyle", WORD_NAMESPACE)
            if paragraph_properties is not None
            else None
        )
        paragraph_bold = _docx_style_bold(
            paragraph_style.get(_word_attr("val")) if paragraph_style is not None else None,
            styles,
        )
        for run in paragraph.findall(".//w:r", WORD_NAMESPACE):
            text = "".join(node.text or "" for node in run.findall(".//w:t", WORD_NAMESPACE)).strip()
            if not text:
                continue
            properties = run.find("w:rPr", WORD_NAMESPACE)
            bold = properties.find("w:b", WORD_NAMESPACE) if properties is not None else None
            is_bold = (
                paragraph_bold
                if bold is None
                else bold.get(_word_attr("val"), "true").casefold() not in {"0", "false", "off", "no"}
            )
            if is_bold:
                emphasized_tokens.extend(normalize_semantic_text(text).split())

    default_language = styles_root.find(
        "w:docDefaults/w:rPrDefault/w:rPr/w:lang",
        WORD_NAMESPACE,
    )
    language = default_language.get(_word_attr("val")) if default_language is not None else None
    drawings = document.findall(f".//{{{WORD_DRAWING_NS}}}docPr")
    missing_alt = [
        node
        for node in drawings
        if not (str(node.get("descr", "")).strip() or str(node.get("title", "")).strip())
    ]
    accessibility = {
        "checked": True,
        "encrypted": False,
        "text_extractable": bool(normalize_semantic_text(extract_docx_text(path))),
        "document_title": _xml_text(core, DC_NS, "title"),
        "document_language": language,
        "external_link_targets_valid": all(_valid_external_target(link) for link in links),
        "nontext_object_count": len(drawings),
        "nontext_alt_text_complete": not missing_alt,
        "tagged": None,
    }
    return links, emphasized_tokens, accessibility


def _pdf_semantic_metadata(path: Path) -> tuple[list[str], list[str], dict[str, Any]]:
    try:
        reader = PdfReader(str(path))
        links: set[str] = set()
        emphasized_tokens: list[str] = []
        image_count = 0
        for page in reader.pages:
            for annotation_reference in page.get("/Annots") or []:
                annotation = annotation_reference.get_object()
                action = annotation.get("/A")
                target = action.get("/URI") if action is not None else None
                if target:
                    links.add(str(target))

            resources = page.get("/Resources") or {}
            xobjects = resources.get("/XObject") or {}
            if hasattr(xobjects, "get_object"):
                xobjects = xobjects.get_object()
            for reference in xobjects.values() if hasattr(xobjects, "values") else []:
                obj = reference.get_object()
                if obj.get("/Subtype") == "/Image":
                    image_count += 1

            def visit_text(text: str, _cm: Any, _tm: Any, font: Any, _size: Any) -> None:
                base_font = str(font.get("/BaseFont", "")) if font else ""
                weight = base_font.casefold()
                if any(marker in weight for marker in ("bold", "semibold", "demi", "black")):
                    emphasized_tokens.extend(normalize_semantic_text(text).split())

            page.extract_text(visitor_text=visit_text)
        metadata = reader.metadata or {}
        catalog = reader.trailer.get("/Root") or {}
        mark_info = catalog.get("/MarkInfo") or {}
        accessibility = {
            "checked": True,
            "encrypted": bool(reader.is_encrypted),
            "text_extractable": all(bool(normalize_semantic_text(page.extract_text() or "")) for page in reader.pages),
            "document_title": str(metadata.get("/Title", "")).strip(),
            "document_language": str(catalog.get("/Lang")) if catalog.get("/Lang") else None,
            "external_link_targets_valid": all(_valid_external_target(link) for link in links),
            "nontext_object_count": image_count,
            "nontext_alt_text_complete": image_count == 0,
            "tagged": bool(mark_info.get("/Marked")) if hasattr(mark_info, "get") else False,
        }
    except Exception as exc:
        raise ValueError(f"Unreadable PDF {path}: {exc}") from exc
    return sorted(links), emphasized_tokens, accessibility


def artifact_metadata(path: Path, artifact_id: str) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text, pages = extract_pdf_text(path)
        external_links, emphasized_tokens, accessibility = _pdf_semantic_metadata(path)
        fmt = "pdf"
    elif suffix == ".docx":
        text = extract_docx_text(path)
        external_links, emphasized_tokens, accessibility = _docx_semantic_metadata(path)
        pages = None
        fmt = "docx"
    else:
        raise ValueError(f"Unsupported artifact format for {path}")
    normalized = normalize_semantic_text(text)
    emphasized = " ".join(emphasized_tokens)
    accessibility["reading_order_sha256"] = sha256_bytes(normalized.encode("utf-8"))
    return {
        "id": artifact_id,
        "filename": path.name,
        "format": fmt,
        "sha256": sha256_file(path),
        "semantic_text_sha256": sha256_bytes(normalized.encode("utf-8")),
        "semantic_word_count": len(normalized.split()),
        "external_links": external_links,
        "emphasis_sha256": sha256_bytes(emphasized.encode("utf-8")),
        "emphasis_word_count": len(emphasized_tokens),
        "accessibility": accessibility,
        "pages": pages,
    }
