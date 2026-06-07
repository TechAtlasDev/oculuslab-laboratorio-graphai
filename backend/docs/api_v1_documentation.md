# Documentación de la API de Grafos (v1)

Esta API permite explorar y analizar un grafo de conocimiento biológico con más de 21 millones de aristas y 190k nodos, utilizando procesamiento optimizado con Polars.

---

## 1. Endpoints de Análisis y Búsqueda

### `GET /api/v1/graph/stats`
Obtiene una visión global del estado del grafo.
- **Respuesta:**
  - `total_nodes`: Cantidad total de entidades.
  - `total_edges`: Cantidad total de relaciones.
  - `nodes_by_label`: Desglose por tipo de nodo (GEN, DIS, DRG, etc.).
  - `edges_by_relation`: Desglose por tipo de relación biológica.

### `GET /api/v1/graph/nodes/search`
Busca nodos por texto (ID, símbolo, nombre o propiedades).
- **Parámetros Query:**
  - `q` (string, requerido): Texto de búsqueda (mín. 2 caracteres).
  - `label` (string, opcional): Filtra por tipo de nodo (ej. `GEN`).
  - `limit` (int, default 20): Máximo de resultados.
- **Uso:** `?q=EGFR&label=GEN`

### `GET /api/v1/graph/nodes/{node_id}`
Obtiene el detalle completo y metadatos JSON de un nodo específico.
- **Uso:** `/api/v1/graph/nodes/ENSG00000146648`
- **Respuesta:** Incluye el objeto `properties` con campos específicos según el tipo de nodo.

### `GET /api/v1/graph/nodes/{node_id}/neighborhood`
Obtiene la vecindad de 1 salto para un nodo, con capacidades de filtrado.
- **Parámetros Query:**
  - `limit` (int, default 15): Cantidad de conexiones.
  - `relation` (string, opcional): Filtrar por relación específica (ej. `INDICATION`).
  - `target_label` (string, opcional): Filtrar por tipo de nodo destino (ej. `DIS`).
- **Uso:** `/api/v1/graph/nodes/CHEMBL1000/neighborhood?relation=INDICATION&target_label=DIS`

---

## 2. Tipos de Nodos y Acciones Semánticas

El sistema identifica el tipo de nodo (`label`) y permite ejecutar acciones específicas basadas en su semántica biológica.

| Tipo (Label) | Descripción | Acciones Sugeridas / Capacidades |
| :--- | :--- | :--- |
| **GEN** | Genes | - Buscar variantes y transcritos.<br>- Analizar expresión en tejidos (`EXPRESSION_PRESENT`).<br>- Identificar dianas terapéuticas. |
| **DRG** | Drogas / Fármacos | - Consultar indicaciones y contraindicaciones.<br>- Ver interacciones sinérgicas con otras drogas.<br>- Consultar propiedades químicas (SMILES, InChI). |
| **DIS** | Enfermedades | - Listar genes asociados (`ASSOCIATED_WITH`).<br>- Ver fenotipos relacionados.<br>- Consultar áreas terapéuticas. |
| **PHE** | Fenotipos | - Identificar enfermedades que presentan el rasgo.<br>- Ver asociaciones génicas. |
| **PWY** | Vías (Pathways) | - Listar todos los genes involucrados en la vía.<br>- Analizar cascadas de señalización. |
| **ANA** | Anatomía | - Ver genes expresados específicamente en ese tejido/órgano. |

---

## 3. Ejemplo de Flujo de Análisis

1. **Descubrimiento:** El usuario busca "Diabetes" usando `/nodes/search?q=diabetes&label=DIS`.
2. **Inspección:** Selecciona el nodo `MESH:D003920` y obtiene sus detalles con `/nodes/{node_id}` para ver su descripción.
3. **Relación Terapéutica:** Consulta qué drogas están indicadas para la diabetes filtrando la vecindad: `/nodes/MESH:D003920/neighborhood?relation=INDICATION&target_label=DRG`.
4. **Métricas:** Analiza qué tan central es la enfermedad en el grafo con `/nodes/{node_id}/metrics`.

---

## Notas de Implementación
- **Lazy Loading:** Las consultas a `edges.parquet` siempre deben estar limitadas (`limit`) para evitar sobrecargar la memoria del cliente.
- **Formatos de ID:** Los IDs suelen seguir estándares (ENSG para genes, CHEMBL para drogas, MESH/DOID para enfermedades).
