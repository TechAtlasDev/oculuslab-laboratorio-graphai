from pydantic import BaseModel, Field
from typing import List

class NodeResponse(BaseModel):
    id: str = Field(..., description="Unique identifier for the node")
    label: str = Field(..., description="Biological label or category of the node")
    display_name: str = Field(..., description="Human-readable name for visualization")

class NodeDetailsResponse(NodeResponse):
    properties: dict = Field(..., description="Full metadata properties of the node")

class EdgeResponse(BaseModel):
    source: str = Field(..., description="ID of the source node")
    target: str = Field(..., description="ID of the target node")
    relation: str = Field(..., description="Type of relationship")

class NeighborhoodResponse(BaseModel):
    node_id: str = Field(..., description="The ID of the queried central node")
    nodes: List[NodeResponse] = Field(..., description="List of unique nodes in the neighborhood")
    edges: List[EdgeResponse] = Field(..., description="List of edges connecting the nodes")

class RelationCount(BaseModel):
    relation: str = Field(..., description="Type of relationship")
    count: int = Field(..., description="Number of edges with this relation")

class NodeMetricsResponse(BaseModel):
    node_id: str = Field(..., description="The ID of the queried node")
    degree: int = Field(..., description="Total number of connections (edges)")
    relations_count: List[RelationCount] = Field(..., description="Breakdown of connections by relation type")

class SearchNodeResponse(BaseModel):
    items: List[NodeResponse] = Field(..., description="List of nodes matching the search criteria")
    total: int = Field(..., description="Total number of matches")

class LabelStat(BaseModel):
    label: str
    count: int

class RelationStat(BaseModel):
    relation: str
    count: int

class GraphStatsResponse(BaseModel):
    total_nodes: int
    total_edges: int
    nodes_by_label: List[LabelStat]
    edges_by_relation: List[RelationStat]
