# Graph API Documentation

## Neighborhood Endpoint

**Endpoint:** `GET /api/v1/graph/nodes/{node_id
}/neighborhood`

### Descripción
Este endpoint recupera el vecindario de grado 1 (conexiones directas) para un nodo específico dentro del grafo de conocimiento biomédico (OptimusKG). Está optimizado para alto rendimiento en servidores backend utilizando *LazyFrames* de Polars, lo que permite realizar consultas extremadamente rápidas sobre los archivos Parquet subyacentes sin sobrecargar la memoria RAM.

### Parámetros de Ruta (Path Parameters)
| Parámetro | Tipo   | Obligatorio | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| `node_id` | `string` | Sí | El identificador único del nodo central del cual se desea conocer su vecindario. | `ENSG00000146648` |

### Parámetros de Consulta (Query Parameters)
| Parámetro | Tipo   | Obligatorio | Rango | Descripción | Por defecto |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `limit` | `integer`| No | 1 - 100 | El número máximo de conexiones (aristas) a recuperar para el nodo indicado. | `15` |

### Estructura de la Respuesta
La respuesta devuelve un objeto JSON estructurado validado estrictamente mediante los modelos de Pydantic (`NeighborhoodResponse`). Este formato divide los resultados en listas separadas para `nodes` y `edges`, haciéndolo óptimo para ser consumido por bibliotecas de renderizado de grafos en el frontend (ej. React Flow, Vis.js o Cytoscape.js).

### Ejemplo de Petición
```bash
curl -X 'GET' \
  'http: //localhost:8000/api/v1/graph/nodes/ENSG00000146648/neighborhood?limit=2' \
  -H 'accept: application/json'
```

### Ejemplo de Respuesta Exitosa (`HTTP 200`)
```json
{
    "node_id": "ENSG00000146648",
    "nodes": [
        {
            "id": "ENSG00000146648",
            "label": "Gene",
            "display_name": "146648"
        },
        {
            "id": "CHEMBL502835",
            "label": "Drug",
            "display_name": "CHEMBL502835"
        },
        {
            "id": "MONDO:0005015",
            "label": "Disease",
            "display_name": "0005015"
        }
    ],
    "edges": [
        {
            "source": "CHEMBL502835",
            "target": "ENSG00000146648",
            "relation": "TARGETS"
        },
        {
            "source": "ENSG00000146648",
            "target": "MONDO:0005015",
            "relation": "ASSOCIATED_WITH"
        }
    ]
}
```

---

## Metrics Endpoint

**Endpoint:** `GET /api/v1/graph/nodes/{node_id
}/metrics`

### Descripción
Este endpoint recupera métricas topológicas para un nodo específico dentro del grafo de conocimiento biomédico. Las métricas incluyen el grado total del nodo (número de conexiones) y un desglose detallado de la cantidad de aristas por tipo de relación. Al igual que el vecindario, este endpoint utiliza *LazyFrames* de Polars para calcular los resultados en tiempo real con alta eficiencia y bajo consumo de memoria RAM.

### Parámetros de Ruta (Path Parameters)
| Parámetro | Tipo   | Obligatorio | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| `node_id` | `string` | Sí | El identificador único del nodo central a analizar. | `ENSG00000146648` |

### Estructura de la Respuesta
La respuesta devuelve un objeto JSON validado mediante el modelo `NodeMetricsResponse` de Pydantic. Contiene el identificador del nodo, su grado (degree) y una lista con la cuenta de ocurrencias por cada tipo de relación.

### Ejemplo de Petición
```bash
curl -X 'GET' \
  'http: //localhost:8000/api/v1/graph/nodes/ENSG00000146648/metrics' \
  -H 'accept: application/json'
```

### Ejemplo de Respuesta Exitosa (`HTTP 200`)
```json
{
    "node_id": "ENSG00000146648",
    "degree": 145,
    "relations_count": [
        {
            "relation": "TARGETS",
            "count": 10
        },
        {
            "relation": "ASSOCIATED_WITH",
            "count": 135
        }
    ]
}
```
