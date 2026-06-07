# Documentación de Metadatos de Nodos (Propiedades)

Cada nodo en el dataset `nodes.parquet` tiene una columna `properties` que contiene un objeto JSON con metadatos específicos según su categoría (`label`). A continuación se detallan los campos más relevantes por tipo de nodo.

---

## 1. GEN (Genes)
Los genes contienen información genómica y funcional detallada.
- **symbol**: Símbolo oficial del gen (ej. `TSPAN6`).
- **name**: Nombre completo del gen.
- **biotype**: Tipo de gen (ej. `protein_coding`).
- **canonical_transcript**: Objeto con ID, cromosoma, posición y hebra del transcrito canónico.
- **synonyms**: Lista de nombres o símbolos alternativos.
- **transcript_ids**: Lista de IDs de transcritos asociados.
- **sources**: Fuentes de los datos (ej. `OPEN_TARGETS`, `BGEE`).

---

## 2. DRG (Drugs / Drogas)
Información química y clínica sobre fármacos.
- **name**: Nombre genérico de la droga (ej. `CETIRIZINE`).
- **type**: Tipo de molécula (ej. `Small molecule`, `Antibody`).
- **inchi_key**: Identificador químico estándar.
- **canonical_smiles**: Notación química SMILES.
- **is_approved**: Booleano que indica si está aprobada.
- **maximum_clinical_trial_phase**: Fase clínica más alta alcanzada.
- **description**: Resumen del fármaco y sus hitos de aprobación.
- **synonyms / trade_names**: Nombres alternativos y comerciales.

---

## 3. DIS (Diseases / Enfermedades)
Metadatos sobre patologías y condiciones.
- **name**: Nombre de la enfermedad.
- **description**: Descripción detallada de la condición.
- **therapeutic_areas**: Áreas terapéuticas relacionadas (ej. enfermedades del sistema nervioso).
- **synonyms (exact, narrow, broad)**: Diferentes niveles de sinonimia.
- **umls_cui / code**: Identificadores en ontologías médicas.

---

## 4. BPO / MFN / CCO (Ontología Génica - GO)
Procesos biológicos, funciones moleculares y componentes celulares.
- **name**: Nombre del término GO.
- **definition**: Definición formal del proceso o función.
- **synonyms**: Términos equivalentes.
- **ontology**: Rama de GO a la que pertenece.
- **xrefs**: Referencias cruzadas a otras bases de datos.

---

## 5. ANA (Anatomy / Anatomía)
Estructuras anatómicas y tejidos.
- **name**: Nombre de la estructura (ej. `gross anatomical part`).
- **definition**: Descripción biológica de la estructura.
- **xrefs**: Referencias (ej. `CARO`, `UBERON`).

---

## 6. PHE (Phenotype / Fenotipo)
Manifestaciones observables o rasgos.
- **name**: Nombre del fenotipo.
- **description**: Descripción del rasgo observado.
- **code / xrefs**: Identificadores en HPO o MeSH.

---

## 7. PWY (Pathway / Vías Metabólicas)
Vías de señalización o procesos metabólicos.
- **name**: Nombre de la vía (ej. `Interleukin-6 signaling`).
- **species**: Especie asociada (ej. `Homo sapiens`).

---

## Notas sobre el procesamiento
La columna `properties` se almacena como `String` en Parquet. Para acceder a estos campos en Python/Polars:
```python
import json
props = json.loads(node_row['properties'])
symbol = props.get('symbol')
```
Debido a la variabilidad de los campos, siempre es recomendable usar `.get()` para evitar errores si una clave no existe en un nodo específico.
