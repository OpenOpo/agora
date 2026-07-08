# Agora OpenOpo

Repositorio público de temarios, referencias normativas y bancos de preguntas para OpenOpo.

La idea es que cualquier persona pueda revisar el contenido, abrir issues, hacer forks y proponer cambios mediante pull requests.

## Entrada pública

El punto de entrada estable para clientes e importadores es:

```text
https://raw.githubusercontent.com/OpenOpo/agora/main/catalog.json
```

El contrato público de importación está documentado en:

```text
docs/import-contract.md
```

## Modelo

Agora separa el contenido en tres capas:

```text
refs/     -> referencias normativas canónicas
syllabi/  -> convocatorias y temarios oficiales
banks/    -> bancos reutilizables de preguntas
```

Regla principal:

```text
La convocatoria no contiene preguntas.
La convocatoria contiene refs normativas exigidas.
La pregunta evalúa refs normativas.
Una pregunta es compatible con un temario si question.refs ∩ syllabus.refs != vacío.
```

## Estructura actual

```text
catalog.json
refs/
  sources.jsonl
  nodes.jsonl
syllabi/
  c1-04-03-64-26/
    syllabus.json
    README.md
banks/
  demo-gva-c1-administrativo/
    bank.json
    questions.jsonl
    README.md
  migrated-c1-04-03-draft/
    bank.json
    questions.jsonl
    README.md
schemas/
  catalog.schema.json
  bank.schema.json
  question.schema.json
  refs.schema.json
  syllabus.schema.json
scripts/
  validate_agora.py
docs/
  import-contract.md
CONTRIBUTING.md
LICENSE
```

## Estados

Los elementos públicos pueden usar estos estados:

- `available`: contenido público e importable.
- `draft`: contenido público para revisión, pero todavía no final.
- `archived`: contenido histórico, no recomendado para importar por defecto.

## Formato de preguntas

Cada línea de `questions.jsonl` es una pregunta JSON independiente.

Ejemplo:

```json
{"statement":"¿Qué reconoce el Título I de la Constitución Española?","correct_answer":"Los derechos y deberes fundamentales.","distractors":["La organización territorial completa del Estado.","El régimen electoral de las entidades locales.","La estructura interna de cada conselleria."],"explanation":"Pregunta demostrativa alineada con una referencia normativa definida en refs/nodes.jsonl.","difficulty":"easy","refs":[{"type":"reference","id":"es-ce-1978::titulo-i"}],"tags":["Constitución","Derechos fundamentales"]}
```

Los `tags` son solo una ayuda de búsqueda y lectura; no sustituyen a `refs`.

## Referencias canónicas

Agora no usa etiquetas libres para enlazar contenido. Cada banco y cada pregunta deben apuntar a referencias canónicas declaradas en:

```text
refs/sources.jsonl
refs/nodes.jsonl
```

Ejemplos de IDs actuales:

- Constitución: `es-ce-1978`.
- Título I de la Constitución: `es-ce-1978::titulo-i`.
- Ley 39/2015: `es-ley-39-2015`.
- Título IV de la Ley 39/2015: `es-ley-39-2015::titulo-iv`.
- Convocatoria C1-04-03 64/26: `c1-04-03::64-26`.

## Validación

Antes de abrir un pull request, ejecuta:

```bash
python scripts/validate_agora.py
```

El validador comprueba JSON/JSONL, refs, compatibilidad básica entre bancos y temarios, y recuentos declarados.

## Contribuir

Consulta `CONTRIBUTING.md` para las reglas básicas de contribución.

No subas contenido si no tienes derecho a usarlo.
