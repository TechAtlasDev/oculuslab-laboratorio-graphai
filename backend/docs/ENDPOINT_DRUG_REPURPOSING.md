# Documentación Detallada: Forward Discovery (Drug Repurposing)

Este endpoint es el núcleo del motor de descubrimiento del backend. Su función es identificar nuevas indicaciones terapéuticas para una droga existente mediante el análisis de caminos de 2 saltos en el grafo de conocimiento.

---

## 1. Concepto y Lógica
El endpoint implementa la técnica de **Reposicionamiento de Fármacos basado en Dianas (Target-based Repurposing)**.

**El Camino:**
`[Droga] --(interactúa con)--> [Gen/Proteína] --(implicado en)--> [Enfermedad]`

Si una droga ya aprobada para la "Enfermedad A" ataca un gen que también está relacionado con la "Enfermedad B", el sistema propone que dicha droga podría ser efectiva para la "Enfermedad B".

---

## 2. Especificación Técnica

### Endpoint
`GET /api/v1/analysis/repurpose/drug/{drug_id}`

### Parámetros
- `drug_id` (Path, String): ID único de la droga en el sistema (ej: `CHEMBL1000`).
- `limit` (Query, Int): Cantidad máxima de candidatos a devolver (default 10, max 50).

### Implementación (Algoritmo de 2 Saltos)
Para garantizar el rendimiento sobre 21 millones de aristas, el servicio realiza las siguientes operaciones en **Polars**:
1. **Filtro de Primer Salto:** Busca todas las aristas en `edges.parquet` conectadas al `drug_id` donde el otro extremo sea un nodo con etiqueta `GEN`.
2. **Filtro de Segundo Salto:** Toma esos genes y busca todas sus aristas conectadas a nodos con etiqueta `DIS` (Enfermedad).
3. **Agregación y Ranking:** Agrupa los resultados por enfermedad y cuenta cuántos genes diferentes conectan la droga con esa enfermedad específica (Evidence Count).

---

## 3. Estructura de Respuesta (JSON)

```json
{
  "drug_id": "CHEMBL1000",
  "candidates": [
    {
      "disease": {
        "id": "EFO_0007355",
        "label": "DIS",
        "display_name": "rinitis alérgica"
      },
      "intermediate_nodes": [
        {
          "id": "ENSG00000085563",
          "label": "GEN",
          "display_name": "HRH1"
        }
      ],
      "evidence_count": 2
    }
  ]
}
```

### Campos de Respuesta:
- `disease`: Información básica del nodo de la enfermedad candidata.
- `intermediate_nodes`: Lista de genes que sirven de puente entre la droga y la enfermedad.
- `evidence_count`: Número de caminos únicos encontrados. A mayor número, mayor es la probabilidad de que la relación sea biológicamente significativa.

---

## 4. Caso de Uso Real: Cetirizina (CHEMBL1000)
Al ejecutar este análisis para la Cetirizina, el sistema identifica:
1. **Dianas:** El receptor de histamina H1 (`HRH1`).
2. **Conexiones:** El sistema encuentra que `HRH1` está vinculado a múltiples condiciones respiratorias e inflamatorias.
3. **Descubrimiento:** El investigador puede ver que la droga no solo sirve para la indicación aprobada, sino que tiene una base molecular sólida para ser investigada en otras patologías conectadas por el mismo gen.

---

## 5. Ventajas para la Presentación
- **Explicabilidad:** No es una "IA de caja negra". El sistema te dice exactamente qué gen (`intermediate_node`) justifica la recomendación.
- **Velocidad:** Gracias a Polars, un análisis de 2 saltos sobre millones de registros se resuelve en milisegundos.
- **Validación:** Los resultados pueden ser validados cruzando los IDs con bases de datos externas como Open Targets o DrugCentral.
