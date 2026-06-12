from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Any, Literal

class BpoSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class OntologyMetadata(BaseModel):
    model_config = ConfigDict(extra='forbid')
    description: Optional[str] = None
    title: Optional[str] = None
    license: Optional[str] = None
    version: Optional[str] = None

class BpoProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: str
    definition: Optional[str] = None
    xrefs: Optional[List[str]] = None
    synonyms: Optional[List[str]] = None
    ontology: Optional[OntologyMetadata] = None
    sources: Optional[BpoSource] = None

class BpoNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["BPO"]
    display_name: str
    properties: BpoProperties
