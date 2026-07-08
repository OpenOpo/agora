# Notas de migración - Modelo v2

## Cambio principal

Se separa claramente:

```text
syllabi/  → convocatorias / temarios oficiales
banks/    → colecciones de preguntas
refs/     → fuentes y nodos normativos
```

## Convocatoria

```text
syllabi/c1-04-03-64-26/syllabus.json
```

ID lógico:

```text
c1-04-03::64-26
```

## Banco migrado

```text
banks/migrated-c1-04-03-draft/questions.jsonl
```

## Resumen

- Fuentes: 12
- Nodos: 38
- Refs del syllabus: 38
- Preguntas incluidas en banco migrado: 2839
- Preguntas excluidas por refs inválidas/fuera de estructura: 193
- Preguntas etiquetadas fuera del syllabus: 95
- Preguntas sin refs pendientes: 689
- Duplicados descartados: 1

## Regla conceptual

La convocatoria incluye refs normativas.  
La pregunta evalúa refs normativas.  
La relación convocatoria-pregunta se calcula por intersección.
