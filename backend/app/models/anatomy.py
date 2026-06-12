from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Literal

class AnatomySource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class AnatomyOntology(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None

class AnatomyProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    definition: Optional[str] = None
    xrefs: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    ontology: Optional[AnatomyOntology] = None
    sources: Optional[AnatomySource] = None

class AnatomyNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["ANA"]
    display_name: str
    properties: AnatomyProperties
