from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Union, Literal

class DiseaseSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class DiseaseProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    description: Optional[str] = None
    code: Optional[str] = None
    umls_cui: Optional[str] = None
    cui_semantic_type: Optional[str] = None
    
    parents: Optional[List[str]] = None
    children: Optional[List[str]] = None
    ancestors: Optional[List[str]] = None
    descendants: Optional[List[str]] = None
    therapeutic_areas: Optional[List[str]] = None
    is_leaf: Optional[bool] = None
    
    exact_synonyms: Optional[List[str]] = None
    related_synonyms: Optional[List[str]] = None
    narrow_synonyms: Optional[List[str]] = None
    broad_synonyms: Optional[List[str]] = None
    
    xrefs: Optional[List[str]] = None
    obsolete_terms: Optional[List[str]] = None
    obsolete_xrefs: Optional[List[str]] = None
    concept_ids: Optional[List[str]] = None
    concept_names: Optional[List[str]] = None
    snomed_full_names: Optional[List[str]] = None
    snomed_concept_ids: Optional[List[Union[str, float]]] = None
    
    sources: Optional[DiseaseSource] = None

class DiseaseNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["DIS"]
    display_name: str
    properties: DiseaseProperties
