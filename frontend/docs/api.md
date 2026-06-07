# 🧬 Guía de Integración API (v0.1.0)

Esta documentación detalla los endpoints disponibles y las estructuras de datos estrictas para el frontend.

## 📌 Endpoints Principales

### `GET /api/v1/graph/discovery/nodes`
**Resumen:** Discover Nodes

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `label` | `query` | `mixed` | ❌ | Filter by node label (e.g. GEN, DRG) |
| `biotype` | `query` | `mixed` | ❌ | Filter genes by biotype (e.g. protein_coding) |
| `chromosome` | `query` | `mixed` | ❌ | Filter genes by chromosome (e.g. X, 1, 2) |
| `is_approved` | `query` | `mixed` | ❌ | Filter drugs by approval status |
| `max_phase` | `query` | `mixed` | ❌ | Filter drugs by max clinical phase |
| `therapeutic_area` | `query` | `mixed` | ❌ | Filter diseases by therapeutic area |
| `limit` | `query` | `integer` | ❌ | - |

### `GET /api/v1/graph/nodes/search`
**Resumen:** Search Nodes

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `q` | `query` | `string` | ✅ | Search query (ID, symbol, or name) |
| `label` | `query` | `mixed` | ❌ | Filter by node label (e.g. GEN, DRG) |
| `limit` | `query` | `integer` | ❌ | - |

### `GET /api/v1/graph/stats`
**Resumen:** Get Graph Stats

### `GET /api/v1/graph/nodes/{node_id}`
**Resumen:** Get Node Details

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `node_id` | `path` | `string` | ✅ | ID of the node to retrieve |

### `GET /api/v1/graph/nodes/{node_id}/neighborhood`
**Resumen:** Get Node Neighborhood

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `node_id` | `path` | `string` | ✅ | ID of the node (e.g. ENSG00000146648) |
| `limit` | `query` | `integer` | ❌ | Max number of connections to retrieve |
| `relation` | `query` | `mixed` | ❌ | Filter by relation type |
| `target_label` | `query` | `mixed` | ❌ | Filter by target node label |

### `GET /api/v1/graph/nodes/{node_id}/metrics`
**Resumen:** Get Node Metrics

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `node_id` | `path` | `string` | ✅ | ID of the node to analyze |

### `GET /api/v1/analysis/repurpose/drug/{drug_id}`
**Resumen:** Drug Repurposing Analysis

| Parámetro | Ubicación | Tipo | Requerido | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `drug_id` | `path` | `string` | ✅ | ID of the drug to analyze (e.g. CHEMBL1000) |
| `limit` | `query` | `integer` | ❌ | - |

### `GET /`
**Resumen:** Root

## 🏗️ Modelos de Datos (Tipado Estricto)

El sistema usa **Uniones Discriminadas**. El campo `label` determina qué propiedades adicionales tendrá el objeto.

### 📦 `GeneProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `symbol` | `string` | - |
| `name` | `complex/any` | - |
| `biotype` | `complex/any` | - |
| `sources` | `complex/any` | - |
| `transcript_ids` | `complex/any` | - |
| `canonical_transcript` | `complex/any` | - |
| `canonical_exons` | `complex/any` | - |
| `genomic_location` | `complex/any` | - |
| `alternative_genes` | `complex/any` | - |
| `synonyms` | `complex/any` | - |
| `symbol_synonyms` | `complex/any` | - |
| `name_synonyms` | `complex/any` | - |
| `obsolete_symbols` | `complex/any` | - |
| `obsolete_names` | `complex/any` | - |
| `associated_proteins` | `complex/any` | - |
| `xrefs` | `complex/any` | - |
| `homologues` | `complex/any` | - |
| `tractability` | `complex/any` | - |
| `constraint_scores` | `complex/any` | - |
| `subcellular_locations` | `complex/any` | - |
| `target_enabling_package` | `complex/any` | - |
| `hallmarks_attributes` | `complex/any` | - |
| `cancer_hallmarks` | `complex/any` | - |
| `chemical_probes` | `complex/any` | - |
| `safety_liabilities` | `complex/any` | - |
| `target_class` | `complex/any` | - |
| `function_descriptions` | `complex/any` | - |
| `transcription_start_site` | `complex/any` | - |

### 📦 `DrugProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `name` | `complex/any` | - |
| `inchi_key` | `complex/any` | - |
| `type` | `complex/any` | - |
| `synonyms` | `complex/any` | - |
| `description` | `complex/any` | - |
| `accession_numbers` | `complex/any` | - |
| `canonical_smiles` | `complex/any` | - |
| `chemical_abstracts_service_number` | `complex/any` | - |
| `unique_ingredient_identifier` | `complex/any` | - |
| `black_box_warning` | `complex/any` | - |
| `year_of_first_approval` | `complex/any` | - |
| `maximum_clinical_trial_phase` | `complex/any` | - |
| `has_been_withdrawn` | `complex/any` | - |
| `is_approved` | `complex/any` | - |
| `trade_names` | `complex/any` | - |
| `sources` | `complex/any` | - |
| `source_ids` | `complex/any` | - |
| `cd_id` | `complex/any` | - |
| `cd_formula` | `complex/any` | - |
| `cd_mol_weight` | `complex/any` | - |
| `calculated_log_p` | `complex/any` | - |
| `alogs` | `complex/any` | - |
| `tpsa` | `complex/any` | - |
| `lipinski` | `complex/any` | - |
| `number_of_formulations` | `complex/any` | - |
| `mol_file_base64` | `complex/any` | - |
| `mol_image_base64` | `complex/any` | - |
| `mrdef` | `complex/any` | - |
| `enhanced_stereo` | `complex/any` | - |
| `aromatic_carbons` | `complex/any` | - |
| `sp3_count` | `complex/any` | - |
| `sp2_count` | `complex/any` | - |
| `sp_count` | `complex/any` | - |
| `halogen_count` | `complex/any` | - |
| `hetero_sp2_count` | `complex/any` | - |
| `rotatable_bonds` | `complex/any` | - |
| `o_n` | `complex/any` | - |
| `oh_nh` | `complex/any` | - |
| `inchi` | `complex/any` | - |
| `rgb` | `complex/any` | - |
| `fda_labels` | `complex/any` | - |
| `status` | `complex/any` | - |
| `struct_id` | `complex/any` | - |

### 📦 `DiseaseProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `name` | `string` | - |
| `description` | `complex/any` | - |
| `code` | `complex/any` | - |
| `umls_cui` | `complex/any` | - |
| `cui_semantic_type` | `complex/any` | - |
| `parents` | `complex/any` | - |
| `children` | `complex/any` | - |
| `ancestors` | `complex/any` | - |
| `descendants` | `complex/any` | - |
| `therapeutic_areas` | `complex/any` | - |
| `is_leaf` | `complex/any` | - |
| `exact_synonyms` | `complex/any` | - |
| `related_synonyms` | `complex/any` | - |
| `narrow_synonyms` | `complex/any` | - |
| `broad_synonyms` | `complex/any` | - |
| `xrefs` | `complex/any` | - |
| `obsolete_terms` | `complex/any` | - |
| `obsolete_xrefs` | `complex/any` | - |
| `concept_ids` | `complex/any` | - |
| `concept_names` | `complex/any` | - |
| `snomed_full_names` | `complex/any` | - |
| `snomed_concept_ids` | `complex/any` | - |
| `sources` | `complex/any` | - |

### 📦 `PharmacologicalProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `source_ids` | `complex/any` | - |
| `source_urls` | `complex/any` | - |
| `mechanisms_of_action` | `complex/any` | - |
| `sources` | `complex/any` | - |

### 📦 `ClinicalProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `highest_clinical_trial_phase` | `complex/any` | - |
| `reference_ids` | `complex/any` | - |
| `sources` | `complex/any` | - |
| `structure_id` | `complex/any` | - |
| `drug_disease_id` | `complex/any` | - |

### 📦 `AssociationProperties`
| Propiedad | Tipo | Descripción |
| :--- | :--- | :--- |
| `evidence_score` | `complex/any` | - |
| `evidence_count` | `complex/any` | - |
| `disgenet_score` | `complex/any` | - |
| `disease_specificity_index` | `complex/any` | - |
| `disease_pleiotropy_index` | `complex/any` | - |
| `evidence_index` | `complex/any` | - |
| `year_initial` | `complex/any` | - |
| `year_final` | `complex/any` | - |
| `sources` | `complex/any` | - |

