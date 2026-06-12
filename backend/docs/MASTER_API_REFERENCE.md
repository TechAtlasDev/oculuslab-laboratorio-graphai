# Master API & Data Reference - Laboratorio de Grafos (v1)

Esta es la documentación técnica definitiva para el backend del Laboratorio de Grafos. Cubre el modelo de datos, los esquemas de metadatos por tipo de entidad y la especificación detallada de los endpoints.

---

## 1. Modelo de Datos de los Datasets

El sistema opera sobre dos archivos Parquet masivos procesados con Polars.

### A. Nodes Dataset (`nodes.parquet`)
- **Estructura base:**
  - `id` (String): Identificador único (ej. `ENSG00000146648`).
  - `label` (String): Categoría biológica.
  - `properties` (JSON String): Metadatos específicos detallados abajo.

### B. Edges Dataset (`edges.parquet`)
- **Estructura base:**
  - `from` (String): ID origen.
  - `to` (String): ID destino.
  - `relation` (String): Tipo de conexión biológica.
  - `undirected` (Boolean): Bidireccionalidad.

---

## 2. Diccionario de Propiedades por Tipo de Nodo (JSON `properties`)

Cada `label` tiene un esquema de propiedades distinto. Los campos más importantes son:

### **GEN (Genes)**
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `symbol` | String | Símbolo oficial (ej. `EGFR`). |
| `name` | String | Nombre descriptivo del gen. |
| `biotype` | String | Tipo (ej. `protein_coding`). |
| `canonical_transcript` | Object | Contiene `id`, `chromosome`, `start`, `end`, `strand`. |
| `synonyms` | List | Nombres alternativos. |

### **DRG (Drugs / Drogas)**
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `name` | String | Nombre genérico (ej. `CETIRIZINE`). |
| `type` | String | `Small molecule`, `Antibody`, etc. |
| `inchi_key` | String | Identificador químico estándar. |
| `is_approved` | Boolean | Estado de aprobación FDA/EMA. |
| `max_phase` | Int | Fase clínica máxima (I, II, III, IV). |

### **DIS (Diseases / Enfermedades)**
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `name` | String | Nombre de la patología. |
| `description` | String | Definición clínica detallada. |
| `therapeutic_areas` | List | Áreas médicas asociadas. |
| `umls_cui` | String | Identificador en Unified Medical Language System. |

### **GO Terms (BPO, MFN, CCO)**
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `name` | String | Título del término de la Ontología Génica. |
| `definition` | String | Definición biológica formal. |

---

## 3. Especificación Detallada de Endpoints

### `GET /api/v1/graph/stats`
Obtiene métricas globales del grafo.
- **Respuesta Exitosa (200):**
```json
{
  "total_nodes": 190531,
  "total_edges": 21813816,
  "nodes_by_label": [{"label": "GEN", "count": 61306}, "..."],
  "edges_by_relation": [{"relation": "ASSOCIATED_WITH", "count": 10531730}, "..."]
}
```

### `GET /api/v1/graph/discovery/nodes`
Endpoint de descubrimiento para filtrar nodos por criterios biológicos y clínicos avanzados.
- **Parámetros:**
  - `label` (String, opcional): Filtrar por tipo (GEN, DRG, DIS).
  - `biotype` (String, opcional): Filtrar genes por biotipo (ej. `protein_coding`). Solo aplica a `label=GEN`.
  - `chromosome` (String, opcional): Filtrar genes por cromosoma (ej. `X`, `21`). Solo aplica a `label=GEN`.
  - `is_approved` (Boolean, opcional): Filtrar drogas por estado de aprobación. Solo aplica a `label=DRG`.
  - `max_phase` (Int, opcional): Filtrar drogas por fase clínica (0-4). Solo aplica a `label=DRG`.
  - `therapeutic_area` (String, opcional): Filtrar enfermedades por área terapéutica. Solo aplica a `label=DIS`.
  - `limit` (Int): Default 20.
- **Respuesta (200):**
```json
{
  "items": [
    {
      "id": "ENSG00000146648",
      "label": "GEN",
      "display_name": "EGFR",
      "properties": { "biotype": "protein_coding", "...": "..." }
    }
  ],
  "total": 1
}
```

### `GET /api/v1/graph/nodes/search`
Búsqueda semántica y por ID.
- **Parámetros:**
  - `q` (Query, String): Texto a buscar.
  - `label` (Query, String, opcional): Filtrar por tipo (GEN, DRG, etc.).
  - `limit` (Query, Int): Default 20.
- **Respuesta (200):**
```json
{
  "items": [
    {
      "id": "ENSG00000146648",
      "label": "GEN",
      "display_name": "EGFR"
    }
  ],
  "total": 1
}
```

### `GET /api/v1/graph/nodes/{node_id}`
Detalle atómico de un nodo.
- **Respuesta (200):**
```json
{
  "id": "ENSG00000146648",
  "label": "GEN",
  "display_name": "ENSG00000146648",
  "properties": {
    "symbol": "EGFR",
    "biotype": "protein_coding",
    "...": "..."
  }
}
```

### `GET /api/v1/graph/nodes/{node_id}/neighborhood`
Navegación por el grafo.
- **Parámetros:**
  - `limit` (Int): Default 15.
  - `relation` (String, opcional): Ej. `TARGETS`.
  - `target_label` (String, opcional): Ej. `DRG`.
- **Respuesta (200):**
```json
{
  "node_id": "ID_CENTRAL",
  "nodes": [{"id": "ID1", "label": "GEN", "display_name": "X"}],
  "edges": [{"source": "ID_CENTRAL", "target": "ID1", "relation": "TYPE"}]
}
```

### `GET /api/v1/graph/nodes/{node_id}/metrics`
Métricas locales del nodo.
- **Respuesta (200):**
```json
{
  "node_id": "ID",
  "degree": 45,
  "relations_count": [{"relation": "EXPRESSION", "count": 40}, {"relation": "INTERACTS", "count": 5}]
}
```

---

## 4. Códigos de Error
- **404 Not Found:** El `node_id` no existe en el dataset.
- **422 Unprocessable Entity:** Parámetros de búsqueda inválidos (ej. query demasiado corta).
- **500 Internal Server Error:** Error en la ejecución de la consulta Polars o fallo de memoria.

---

## 5. Recomendaciones de Consumo
1. **Paginación Visual:** El frontend debe usar el `limit` de la vecindad para no saturar el renderizado del grafo.
2. **Caché:** Se recomienda cachear los resultados de `/stats` ya que cambian con poca frecuencia.
3. **Búsqueda:** Utilizar la búsqueda con filtro de `label` siempre que sea posible para acelerar la respuesta.
