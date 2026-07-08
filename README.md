# Agora OpenOpo

Repositorio público de bancos de preguntas para OpenOpo.

La idea es que cualquier persona pueda revisar el contenido, abrir issues, hacer forks y proponer cambios mediante pull requests.

La especificación completa de referencias canónicas está en `docs/AGORA_REFERENCIAS_CANONICAS.md` dentro del proyecto OpenOpo.

## Estructura

```text
catalog.json
refs/
  oppositions.json
  legal-sources.json
  legal-articles.jsonl
banks/
  demo-gva-c1-administrativo/
    bank.json
    questions.jsonl
    README.md
syllabi/
  gva-c1-04-03-64-26/
    syllabus.json
    README.md
schemas/
  catalog.schema.json
  bank.schema.json
  question.schema.json
  refs.schema.json
  syllabus.schema.json
CONTRIBUTING.md
LICENSE
```

## Formato de preguntas

Cada línea de `questions.jsonl` es una pregunta:

```json
{"statement":"Pregunta...","correct_answer":"Respuesta correcta","distractors":["Opción 1","Opción 2","Opción 3"],"explanation":"Explicación opcional","difficulty":"medium","refs":[{"type":"legal_article","id":"es-ley-39-2015-art-14"},{"type":"syllabus_node","id":"gva-c1-04-03-64-26:tema-01"}],"tags":["Ley 39/2015","Artículo 14"]}
```

## Referencias canónicas

Agora no usa etiquetas libres para enlazar contenido. Cada banco y cada pregunta deben apuntar a referencias canónicas de OpenOpo.

Ejemplos de IDs:

- Convocatoria: `gva-c1-04-03-64-26`.
- Parte o bloque: `gva-c1-04-03-64-26:parte-general`.
- Tema: `gva-c1-04-03-64-26:tema-01`.
- Ley: `es-ley-39-2015`.
- Artículo: `es-ley-39-2015-art-14`.

Los `tags` son solo una ayuda de búsqueda y lectura; no sustituyen a `refs`.

## Temarios públicos

Los temarios también pueden vivir en este repositorio para que la comunidad proponga cambios mediante pull requests.

Cada convocatoria debería tener su propia carpeta estable:

```text
syllabi/
  gva-c1-04-03-64-26/
    syllabus.json
    README.md
  gva-c1-04-03-70-25/
    syllabus.json
    README.md
  gva-c2-03-03/
    syllabus.json
    README.md
```

Ejemplo mínimo de `syllabus.json`:

```json
{
  "schema_version": 1,
  "id": "gva-c1-04-03-64-26",
  "title": "GVA C1-04-03 convocatoria 64/26",
  "opposition": "Generalitat Valenciana",
  "level": "C1",
  "call": "64/26",
  "blocks": [
    {
      "id": "gva-c1-04-03-64-26:parte-general",
      "title": "Parte general",
      "items": [
        {
          "id": "gva-c1-04-03-64-26:tema-01",
          "title": "Tema 1",
          "refs": ["es-ley-39-2015-art-14"]
        }
      ]
    }
  ]
}
```
