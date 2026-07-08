# Agora public import contract

This document describes the stable public contract for clients that want to import public Agora content.

Agora is organized into three layers:

```text
refs/     -> canonical normative references
syllabi/  -> official call syllabi and their required refs
banks/    -> reusable question banks
```

A syllabus does not own questions. A question points to canonical refs. A bank is compatible with a syllabus when the question refs intersect the syllabus refs.

## Public entry point

The public entry point is:

```text
https://raw.githubusercontent.com/OpenOpo/agora/main/catalog.json
```

Clients should load `catalog.json` first and then follow the paths and URLs declared there.

## Catalog fields

Top-level fields:

- `version`: catalog format version.
- `updated_at`: last catalog update date.
- `syllabi`: list of available or draft syllabi.
- `banks`: list of available or draft banks.

A `syllabi[]` entry contains:

- `id`: stable syllabus id, for example `c1-04-03::64-26`.
- `title`: human-readable title.
- `path`: repository-relative path to the syllabus JSON file.
- `status`: `available`, `draft`, or `archived`.
- `source_url`: official source URL when available.
- `refs_count`: number of canonical refs included in the syllabus.

A `banks[]` entry contains:

- `id`: stable bank id.
- `title`: human-readable title.
- `description`: short public description.
- `question_count`: expected number of questions.
- `scope`: declared refs covered by the bank.
- `compatible_syllabi`: syllabus ids this bank can be used with.
- `questions_url`: raw URL to the bank `questions.jsonl` file.
- `github_url`: repository URL for review and contributions.
- `issues_url`: issue tracker URL.
- `status`: `available`, `draft`, or `archived`.

## Status meanings

- `available`: content is public and intended for import.
- `draft`: content is public for review but not yet considered final.
- `archived`: content is kept for history but should not be offered by default.

Importing clients may choose to show `draft` content behind an explicit experimental or review flag.

## Questions JSONL

Each `questions.jsonl` file is newline-delimited JSON. Each non-empty line is one question object.

Minimal fields:

- `id`: stable question id when available.
- `statement`: question text.
- `correct_answer`: correct answer.
- `distractors`: list of wrong answers.
- `explanation`: optional explanation.
- `difficulty`: `easy`, `medium`, or `hard`.
- `refs`: list of canonical reference objects.
- `tags`: search/display tags only.

Example:

```json
{"statement":"¿Qué reconoce el Título I de la Constitución Española?","correct_answer":"Los derechos y deberes fundamentales.","distractors":["La organización territorial completa del Estado.","El régimen electoral de las entidades locales.","La estructura interna de cada conselleria."],"explanation":"Pregunta demostrativa alineada con una referencia normativa definida en refs/nodes.jsonl.","difficulty":"easy","refs":[{"type":"reference","id":"es-ce-1978::titulo-i"}],"tags":["Constitución","Derechos fundamentales"]}
```

## Reference resolution

Clients should resolve refs using:

```text
refs/sources.jsonl
refs/nodes.jsonl
```

A question ref is valid when its `id` exists in either `refs/sources.jsonl` or `refs/nodes.jsonl`.

A question is compatible with a syllabus when:

```text
question.refs ∩ syllabus.refs != empty
```

## Validation

Repository content can be validated with:

```bash
python scripts/validate_agora.py
```

For importers, a non-zero validator exit code means the catalog should not be published as an importable update.

## Client recommendations

Clients should:

- Treat ids as stable identifiers.
- Treat `tags` as display/search metadata only.
- Prefer `questions_url` for downloading bank questions.
- Respect `status` when deciding what to show to users.
- Keep local imports immutable when possible, storing the catalog version/date used.
- Avoid assuming that one bank belongs to only one syllabus.
