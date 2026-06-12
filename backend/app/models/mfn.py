from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Literal

class MfnSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class MfnOntology(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None

class MfnProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    definition: Optional[str] = None
    xrefs: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    ontology: Optional[MfnOntology] = None
    sources: Optional[MfnSource] = None

class MfnNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["MFN"]
    display_name: str
    properties: MfnProperties
