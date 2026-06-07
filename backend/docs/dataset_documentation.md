# Documentación de Datasets (OptimusKG)

Esta documentación describe el contenido de los datasets de grafos utilizados en el laboratorio, analizados mediante el script `scripts/inspect_datasets.py`.

## Resumen General

| Dataset | Filas | Propósito |
|---------|-------|-----------|
| `nodes.parquet` | 190,531 | Información de entidades (Genes, Enfermedades, Drogas, etc.) |
| `edges.parquet` | 21,813,816 | Relaciones biológicas entre las entidades |

---

## 1. Nodes Dataset (`nodes.parquet`)

### Esquema
- **id** (String): Identificador único del nodo (ej. `ENSG00000146648`, `MESH_D003920`).
- **label** (String): Categoría biológica abreviada.
- **properties** (String): JSON con metadatos adicionales (nombres comunes, descripciones, etc.).

### Entidades Principales (Top Labels)
El dataset contiene diversos tipos de entidades biológicas:

1. **GEN (Gene):** 61,306 nodos.
2. **DIS (Disease):** 36,345 nodos.
3. **BPO (Biological Process):** 25,754 nodos.
4. **PHE (Phenotype):** 19,341 nodos.
5. **DRG (Drug):** 16,766 nodos.
6. **ANA (Anatomy):** 13,120 nodos.
7. **MFN (Molecular Function):** 10,161 nodos.

---

## 2. Edges Dataset (`edges.parquet`)

### Esquema
- **from** (String): ID del nodo origen.
- **to** (String): ID del nodo destino.
- **label** (String): Etiqueta general de la arista.
- **relation** (String): Tipo específico de relación biológica.
- **undirected** (Boolean): Indica si la relación es bidireccional.
- **properties** (String): JSON con metadatos de la relación (puntuaciones, fuentes, etc.).

### Relaciones Principales (Top Relations)
El grafo es denso, con más de 21 millones de conexiones:

1. **ASSOCIATED_WITH:** 10,531,730 (Relación general de asociación).
2. **EXPRESSION_PRESENT:** 6,616,463 (Presencia de expresión génica en tejidos).
3. **EXPRESSION_ABSENT:** 2,171,492 (Ausencia de expresión).
4. **SYNERGISTIC_INTERACTION:** 1,341,086 (Interacciones sinérgicas, común entre drogas).
5. **INTERACTS_WITH:** 734,862 (Interacciones proteína-proteína o general).
6. **PHENOTYPE_PRESENT:** 157,144 (Asociación con fenotipos).
7. **INDICATION:** 58,690 (Indicaciones terapéuticas de drogas).

---

## Notas Técnicas
- Los archivos se procesan de manera perezosa (Lazy) usando **Polars** para minimizar el impacto en memoria, dado el tamaño de `edges.parquet` (~22M de filas).
- Para análisis detallados, se recomienda filtrar por `relation` o `label` antes de recolectar los datos (`.collect()`).
