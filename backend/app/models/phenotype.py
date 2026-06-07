from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union

class PhenotypeSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class PhenotypeOntology(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None

class PhenotypeProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    description: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
    
    # Jerarquía
    parents: Optional[List[str]] = None
    children: Optional[List[str]] = None
    ancestors: Optional[List[str]] = None
    descendants: Optional[List[str]] = None
    
    # Sinónimos
    exact_synonyms: Optional[List[str]] = None
    related_synonyms: Optional[List[str]] = None
    narrow_synonyms: Optional[List[str]] = None
    broad_synonyms: Optional[List[str]] = None
    
    # Identificadores Médicos
    umls_cui: Optional[str] = None
    cui_semantic_type: Optional[str] = None
    concept_ids: Optional[List[str]] = None
    concept_names: Optional[List[str]] = None
    snomed_concept_ids: Optional[List[Union[str, float]]] = None
    snomed_full_names: Optional[List[str]] = None
    
    # Referencias y Metadatos
    xrefs: Optional[List[str]] = None
    obsolete_terms: Optional[List[str]] = None
    obsolete_xrefs: Optional[List[str]] = None
    ontology: Optional[PhenotypeOntology] = None
    sources: Optional[PhenotypeSource] = None

class PhenotypeNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: str # Debe ser "PHE"
    properties: PhenotypeProperties
