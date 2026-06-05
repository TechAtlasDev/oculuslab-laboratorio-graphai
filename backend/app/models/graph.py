from pydantic import BaseModel, Field
from typing import List

class NodeResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    label: str = Field(..., description="Biological label or category of the node")
    display_name: str = Field(..., description="Human-readable name for visualization")

class EdgeResponse(BaseModel):
    source: str = Field(..., description="ID of the source node")
    target: str = Field(..., description="ID of the target node")
    relation: str = Field(..., description="Type of relationship")

class NeighborhoodResponse(BaseModel):
    node_id: str = Field(..., description="The ID of the queried central node")
    nodes: List[NodeResponse] = Field(..., description="List of unique nodes in the neighborhood")
    edges: List[EdgeResponse] = Field(..., description="List of edges connecting the nodes")
