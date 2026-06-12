from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal

class PwySource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class PwyProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: Optional[str] = None
    species: Optional[str] = None
    sources: Optional[PwySource] = None

class PathwayNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: Literal["PWY"]
    display_name: str
    properties: PwyProperties
