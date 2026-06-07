from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union

class EdgeSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

# Propiedades para TARGETS, AGONIST, INHIBITOR, etc.
class PharmacologicalProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    source_ids: Optional[List[str]] = None
    source_urls: Optional[List[str]] = None
    mechanisms_of_action: Optional[List[str]] = None
    sources: Optional[EdgeSource] = None

# Propiedades para INDICATION, CONTRAINDICATION, OFF_LABEL_USE
class ClinicalProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    highest_clinical_trial_phase: Optional[float] = None
    reference_ids: Optional[List[str]] = None
    sources: Optional[EdgeSource] = None
    structure_id: Optional[str] = None
    drug_disease_id: Optional[str] = None

# Propiedades para ASSOCIATED_WITH
class AssociationProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    evidence_score: Optional[float] = None
    evidence_count: Optional[int] = None
    disgenet_score: Optional[float] = None
    disease_specificity_index: Optional[float] = None
    disease_pleiotropy_index: Optional[float] = None
    evidence_index: Optional[float] = None
    year_initial: Optional[Union[int, float]] = None
    year_final: Optional[Union[int, float]] = None
    sources: Optional[EdgeSource] = None

# Propiedades para EXPRESSION_PRESENT / ABSENT
class ExpressionProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    expression_rank: Optional[int] = None
    call_quality: Optional[str] = None
    sources: Optional[EdgeSource] = None

# Propiedades para SYNERGISTIC_INTERACTION
class InteractionProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    interaction_description: Optional[str] = None
    sources: Optional[EdgeSource] = None

# Propiedades base para relaciones simples (Ontología, etc.)
class BaseEdgeProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    sources: Optional[EdgeSource] = None
    evidence: Optional[List[str]] = None
    gene_product: Optional[List[str]] = None
    eco_ids: Optional[List[str]] = None
    aspect: Optional[List[str]] = None
    bio_curation: Optional[List[str]] = None
    evidence_type: Optional[List[str]] = None
    frequency: Optional[List[str]] = None
    qualifier_not: Optional[bool] = None
    references: Optional[List[str]] = None
    modifiers: Optional[List[str]] = None
    onset: Optional[List[str]] = None
    # Campos extra detectados en el descubrimiento
    source_ids: Optional[List[str]] = None
    source_urls: Optional[List[str]] = None
    highest_clinical_trial_phase: Optional[float] = None
    reference_ids: Optional[List[str]] = None
    structure_id: Optional[str] = None
    drug_disease_id: Optional[str] = None

class Edge(BaseModel):
    model_config = ConfigDict(extra='forbid')
    from_id: str = Field(..., alias="from")
    to_id: str = Field(..., alias="to")
    relation: str
    label: str # Ej: "DRG-GEN"
    undirected: bool
    properties: Union[
        PharmacologicalProperties,
        ClinicalProperties,
        AssociationProperties,
        ExpressionProperties,
        InteractionProperties,
        BaseEdgeProperties,
        Any
    ]
