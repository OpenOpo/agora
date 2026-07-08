# Agora y referencias canónicas OpenOpo

Este documento define la estructura que debe seguir Agora para evitar que los bancos de preguntas, temarios, leyes y artículos acaben siendo un cajón desastre.

## Objetivo

OpenOpo es la herramienta privada de estudio. Agora es la fuente pública y revisable de contenido.

La regla principal es simple: una pregunta no debe depender solo de etiquetas libres como `Ley 39/2015` o `Tema 1`. Debe apuntar a referencias canónicas de OpenOpo mediante IDs estables.

Los `tags` siguen existiendo, pero solo como ayuda de búsqueda y lectura.

## Estructura del repositorio Agora

```text
agora/
  catalog.json
  refs/
    oppositions.json
    legal-sources.json
    legal-articles.jsonl
  syllabi/
    gva-c1-04-03-64-26/
      syllabus.json
      README.md
  banks/
    ley-39-2015-art-14-repaso/
      bank.json
      questions.jsonl
      README.md
  schemas/
    catalog.schema.json
    bank.schema.json
    question.schema.json
    refs.schema.json
    syllabus.schema.json
  CONTRIBUTING.md
  LICENSE
  README.md
```

## IDs canónicos

Los IDs deben ser legibles, estables, en minúsculas y ASCII.

Ejemplos:

```text
gva-c1-04-03-64-26
gva-c1-04-03-64-26:parte-general
gva-c1-04-03-64-26:tema-01
es-ley-39-2015
es-ley-39-2015-art-14
```

Reglas:

- No usar UUIDs opacos si el ID puede ser legible.
- No cambiar un ID una vez publicado salvo error grave.
- No usar acentos, espacios ni mayúsculas.
- Usar `:` para nodos internos de temario de una convocatoria.
- Usar `-` para leyes, artículos y slugs generales.

## Registros de referencias

`refs/oppositions.json` contiene oposiciones y convocatorias:

```json
{
  "schema_version": 1,
  "items": [
    {
      "id": "gva-c1-04-03-64-26",
      "title": "GVA C1-04-03 convocatoria 64/26",
      "administration": "Generalitat Valenciana",
      "level": "C1",
      "call": "64/26"
    }
  ]
}
```

`refs/legal-sources.json` contiene leyes o normas:

```json
{
  "schema_version": 1,
  "items": [
    {
      "id": "es-ley-39-2015",
      "title": "Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas",
      "short_title": "Ley 39/2015",
      "jurisdiction": "ES"
    }
  ]
}
```

`refs/legal-articles.jsonl` contiene artículos o fragmentos:

```jsonl
{"id":"es-ley-39-2015-art-14","source_id":"es-ley-39-2015","title":"Artículo 14. Derecho y obligación de relacionarse electrónicamente con las Administraciones Públicas"}
```

## Temarios públicos

Cada convocatoria tiene su propio `syllabus.json`.

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

Un temario puede enlazar con leyes, artículos o fragmentos mediante `refs`.

## Bancos de preguntas

Cada banco declara su alcance mediante `scope`.

Ejemplo de banco de un artículo:

```json
{
  "schema_version": 1,
  "id": "ley-39-2015-art-14-repaso",
  "title": "Ley 39/2015 - Artículo 14",
  "description": "Preguntas de repaso sobre el artículo 14.",
  "level": "C1",
  "question_count": 120,
  "scope": {
    "type": "legal_article",
    "refs": ["es-ley-39-2015-art-14"]
  },
  "compatible_syllabi": ["gva-c1-04-03-64-26"],
  "questions_file": "questions.jsonl",
  "status": "available"
}
```

Tipos de alcance permitidos:

- `opposition`: banco de una oposición o convocatoria completa.
- `syllabus_node`: banco de una parte, bloque o tema.
- `legal_source`: banco de una ley o norma completa.
- `legal_article`: banco de un artículo o fragmento concreto.
- `mixed`: banco mixto con varias referencias.

## Preguntas

Cada línea de `questions.jsonl` es una pregunta JSON válida.

```json
{
  "statement": "Pregunta...",
  "correct_answer": "Respuesta correcta",
  "distractors": ["Opción 1", "Opción 2", "Opción 3"],
  "explanation": "Explicación opcional",
  "difficulty": "medium",
  "refs": [
    {"type": "legal_article", "id": "es-ley-39-2015-art-14"},
    {"type": "syllabus_node", "id": "gva-c1-04-03-64-26:tema-01"}
  ],
  "tags": ["Ley 39/2015", "Artículo 14"]
}
```

Reglas:

- En Agora, toda pregunta debe tener `statement`, `correct_answer` y al menos una referencia en `refs`.
- Las referencias de `refs` deben existir en `refs/` o en algún `syllabus.json`.
- `tags` no se usan para validar compatibilidad con temarios.

## Validación en OpenOpo

OpenOpo debe aplicar estas reglas:

- El catálogo debe ser JSON válido.
- Cada banco debe tener `id`, `title`, `question_count`, `questions_url` y `scope`.
- Cada `scope.refs[]` debe existir en los registros canónicos.
- Los bancos sin referencias válidas se marcan como `Necesita revisión` y no son importables desde Biblioteca.
- Al importar desde Agora, cada pregunta debe tener referencias canónicas.
- Las subidas personales pueden no tener referencias, pero se importan con aviso y quedan como contenido privado menos estructurado.

## Datos guardados al importar

Al importar un banco, OpenOpo guarda en el perfil privado del usuario:

- preguntas cifradas;
- `question_hash`;
- `package_key`;
- `refs`;
- `tags`;
- metadatos del paquete, como `scope` y `compatible_syllabi`.

OpenOpo no convierte las preguntas importadas en contenido público de WordPress.

## Filosofía

Agora ordena y valida el contenido público.

OpenOpo interpreta ese contenido, lo cifra para el usuario y lo convierte en estudio privado.

La responsabilidad del contenido importado sigue estando en quien lo aporta o lo importa, pero la plataforma evita el caos estructural exigiendo referencias canónicas en la Biblioteca pública.
