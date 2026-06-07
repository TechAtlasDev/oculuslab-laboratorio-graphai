from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class ExpSource(BaseModel):
    model_config = ConfigDict(extra='forbid')
    direct: Optional[List[str]] = None
    indirect: Optional[List[str]] = None

class ExpProperties(BaseModel):
    model_config = ConfigDict(extra='forbid')
    
    name: Optional[str] = None
    source_categories: Optional[List[str]] = None
    source_details: Optional[str] = None
    sources: Optional[ExpSource] = None

class ExposureNode(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str
    label: str # Debe ser "EXP"
    properties: ExpProperties
