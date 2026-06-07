from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any

class CcoSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class CcoOntology(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None

class CcoProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    definition: Optional[str] = None
    xrefs: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    ontology: Optional[CcoOntology] = None
    sources: Optional[CcoSource] = None

class CcoNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: str # Debe ser "CCO"
    properties: CcoProperties
