# Propuesta Técnica: Módulo de Análisis de Redes y Reposicionamiento de Fármacos

Este documento detalla la estrategia para implementar herramientas de descubrimiento biológico avanzado sobre el grafo de OptimusKG, utilizando los principios de la **Farmacología de Redes**.

---

## 1. Visión General
El objetivo es transformar el backend de un simple visor de datos a un **motor de descubrimiento**. El reposicionamiento de fármacos busca identificar nuevas indicaciones terapéuticas para drogas existentes basándose en las conexiones indirectas (caminos) dentro del grafo de conocimiento.

## 2. Lógica Farmacológica (Network Pharmacology)
La hipótesis central se basa en la transitividad de las relaciones:
- **Relación 1:** La `Droga A` interactúa con el `Gen X` (ej. relación `TARGETS` o `INTERACTS_WITH`).
- **Relación 2:** El `Gen X` está implicado en la `Enfermedad B` (ej. relación `ASSOCIATED_WITH`).
- **Inferencia:** La `Droga A` tiene un potencial terapéutico para la `Enfermedad B`.

## 3. Especificación de Endpoints Propuestos

### A. Reposicionamiento Directo (Forward Discovery)
- **Endpoint:** `GET /api/v1/analysis/repurpose/drug/{drug_id}`
- **Entrada:** ID de una Droga.
- **Salida:** Lista de enfermedades potenciales conectadas a través de genes comunes.
- **Uso:** Identificar qué otras enfermedades podría tratar una droga conocida.

### B. Reposicionamiento Inverso (Reverse Discovery)
- **Endpoint:** `GET /api/v1/analysis/repurpose/disease/{disease_id}`
- **Entrada:** ID de una Enfermedad.
- **Salida:** Lista de drogas candidatas que atacan genes asociados a esa enfermedad.
- **Uso:** Encontrar fármacos existentes para una enfermedad específica.

### C. Evidencia de Camino (Path Evidence)
- **Endpoint:** `GET /api/v1/analysis/evidence/{source_id}/{target_id}`
- **Entrada:** Dos IDs (ej. Droga y Enfermedad).
- **Salida:** Los "puentes" (genes) exactos y las relaciones que justifican la conexión.
- **Uso:** Transparencia y validación científica.

### D. Enriquecimiento de Dianas (Target Enrichment)
- **Endpoint:** `GET /api/v1/analysis/enrichment/target/{gene_id}`
- **Entrada:** ID de un Gen.
- **Salida:** Estadísticas de centralidad (cuántas drogas lo atacan vs. cuántas enfermedades afecta).
- **Uso:** Validar si un gen es una diana prometedora.

## 4. Estrategia de Implementación Técnica
Se utilizará **Polars** para realizar operaciones de unión (*Joins*) masivas en memoria sobre los archivos Parquet.

1. **Lazy Loading:** Escaneo perezoso de `edges.parquet` y `nodes.parquet`.
2. **Double Join:**
   - Paso 1: Filtrar aristas donde el origen es la Droga.
   - Paso 2: Unir el resultado con las aristas donde el origen es el Gen resultante y el destino es una Enfermedad.
3. **Optimización:** Se filtrará por `label` (GEN, DIS, DRG) antes de realizar el join para reducir el espacio de búsqueda.

## 5. Validación
El sistema no es experimental en el sentido de "adivinar", sino que **reporta conexiones existentes pero no evidentes**. La validación se realiza mediante los `xrefs` (referencias externas) presentes en los metadatos de las aristas y nodos involucrados en el camino.
