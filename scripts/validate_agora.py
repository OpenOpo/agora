#!/usr/bin/env python3
"""Validate Agora catalog, refs, syllabi and banks.

Stdlib-only validator for local use and CI.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def load_json(path: Path, reporter: Reporter) -> Any | None:
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        reporter.error(f"Missing file: {path}")
    except json.JSONDecodeError as exc:
        reporter.error(f"Invalid JSON in {path}:{exc.lineno}:{exc.colno}: {exc.msg}")
    return None


def load_jsonl(path: Path, reporter: Reporter) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError as exc:
                    reporter.error(f"Invalid JSONL in {path}:{lineno}:{exc.colno}: {exc.msg}")
                    continue
                if not isinstance(value, dict):
                    reporter.error(f"JSONL row is not an object: {path}:{lineno}")
                    continue
                rows.append(value)
    except FileNotFoundError:
        reporter.error(f"Missing file: {path}")
    return rows


def collect_refs(root: Path, reporter: Reporter) -> set[str]:
    ref_ids: set[str] = set()
    for rel in ["refs/sources.jsonl", "refs/nodes.jsonl"]:
        path = root / rel
        if not path.exists():
            reporter.warn(f"Reference file not found: {rel}")
            continue
        for row in load_jsonl(path, reporter):
            ref_id = row.get("id")
            if isinstance(ref_id, str):
                if ref_id in ref_ids:
                    reporter.error(f"Duplicate ref id: {ref_id}")
                ref_ids.add(ref_id)
            else:
                reporter.error(f"Reference row without string id in {rel}")
    return ref_ids


def walk_syllabus_refs(node: dict[str, Any]) -> set[str]:
    refs = set(r for r in node.get("refs", []) if isinstance(r, str))
    for child in node.get("items", []) or []:
        if isinstance(child, dict):
            refs |= walk_syllabus_refs(child)
    return refs


def validate_syllabi(
    root: Path,
    catalog: dict[str, Any],
    known_refs: set[str],
    reporter: Reporter,
) -> dict[str, set[str]]:
    syllabus_refs: dict[str, set[str]] = {}

    for entry in catalog.get("syllabi", []) or []:
        if not isinstance(entry, dict):
            reporter.error("catalog.syllabi contains a non-object entry")
            continue

        sid = entry.get("id")
        path_value = entry.get("path")
        if not isinstance(sid, str) or not isinstance(path_value, str):
            reporter.error("catalog.syllabi entry must include string id and path")
            continue

        data = load_json(root / path_value, reporter)
        if not isinstance(data, dict):
            continue

        if data.get("id") != sid:
            reporter.error(
                f"Syllabus id mismatch for {path_value}: "
                f"catalog={sid!r}, file={data.get('id')!r}"
            )

        refs: set[str] = set()
        for block in data.get("blocks", []) or []:
            if isinstance(block, dict):
                refs |= walk_syllabus_refs(block)

        syllabus_refs[sid] = refs

        for ref in sorted(refs - known_refs):
            reporter.error(f"Syllabus {sid} uses undefined ref: {ref}")

        expected = entry.get("refs_count")
        if isinstance(expected, int) and expected != len(refs):
            reporter.error(
                f"Syllabus {sid} refs_count mismatch: "
                f"catalog={expected}, actual={len(refs)}"
            )

    return syllabus_refs


def question_ref_ids(question: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for ref in question.get("refs", []) or []:
        if isinstance(ref, dict) and isinstance(ref.get("id"), str):
            ids.add(ref["id"])
    return ids


def validate_bank(
    root: Path,
    entry: dict[str, Any],
    known_refs: set[str],
    syllabus_refs: dict[str, set[str]],
    reporter: Reporter,
) -> None:
    bank_id = entry.get("id")
    if not isinstance(bank_id, str):
        reporter.error("catalog.banks entry without string id")
        return

    manifest_path = root / "banks" / bank_id / "bank.json"
    manifest = load_json(manifest_path, reporter)
    if not isinstance(manifest, dict):
        return

    if manifest.get("id") != bank_id:
        reporter.error(
            f"Bank id mismatch for {manifest_path}: "
            f"catalog={bank_id!r}, file={manifest.get('id')!r}"
        )

    questions_file = manifest.get("questions_file")
    if isinstance(questions_file, str):
        questions_path = manifest_path.parent / questions_file
    else:
        questions_path = manifest_path.parent / "questions.jsonl"

    questions = load_jsonl(questions_path, reporter)

    expected_count = manifest.get("question_count", entry.get("question_count"))
    if isinstance(expected_count, int) and expected_count != len(questions):
        reporter.error(
            f"Bank {bank_id} question_count mismatch: "
            f"manifest={expected_count}, actual={len(questions)}"
        )

    duplicate_ids: set[str] = set()
    seen_ids: set[str] = set()

    compatible = [
        s
        for s in manifest.get("compatible_syllabi", []) or []
        if isinstance(s, str)
    ]
    known_compatible_refs = set().union(
        *(syllabus_refs[s] for s in compatible if s in syllabus_refs)
    )

    for index, question in enumerate(questions, 1):
        prefix = f"{questions_path}:{index}"

        for field in ["statement", "correct_answer", "refs"]:
            if field not in question:
                reporter.error(f"{prefix}: missing required field {field!r}")

        qid = question.get("id")
        if isinstance(qid, str):
            if qid in seen_ids:
                duplicate_ids.add(qid)
            seen_ids.add(qid)

        refs = question_ref_ids(question)
        if not refs:
            reporter.error(f"{prefix}: question has no usable refs")

        for ref in sorted(refs - known_refs):
            reporter.warn(f"{prefix}: question uses ref not defined in refs/: {ref}")

        if known_compatible_refs and refs.isdisjoint(known_compatible_refs):
            reporter.error(f"{prefix}: refs do not intersect compatible syllabus refs")

    for qid in sorted(duplicate_ids):
        reporter.error(f"Bank {bank_id} has duplicate question id: {qid}")


def validate(root: Path) -> Reporter:
    reporter = Reporter()

    catalog = load_json(root / "catalog.json", reporter)
    if not isinstance(catalog, dict):
        return reporter

    known_refs = collect_refs(root, reporter)
    syllabus_refs = validate_syllabi(root, catalog, known_refs, reporter)

    banks = catalog.get("banks")
    if not isinstance(banks, list):
        reporter.error("catalog.banks must be an array")
        return reporter

    for entry in banks:
        if isinstance(entry, dict):
            validate_bank(root, entry, known_refs, syllabus_refs, reporter)
        else:
            reporter.error("catalog.banks contains a non-object entry")

    return reporter


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agora repository checkout")
    parser.add_argument("root", nargs="?", default=".", help="Repository root directory")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat warnings as errors",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    reporter = validate(root)

    for warning in reporter.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in reporter.errors:
        print(f"ERROR: {error}", file=sys.stderr)

    print(
        f"Validation complete: "
        f"{len(reporter.errors)} error(s), {len(reporter.warnings)} warning(s)"
    )

    if reporter.errors or (args.strict_warnings and reporter.warnings):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
