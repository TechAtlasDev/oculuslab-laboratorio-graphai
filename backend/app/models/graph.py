from pydantic import BaseModel, Field, ConfigDict
from typing import List, Union, Annotated
from app.models.gene import GeneNode
from app.models.drug import DrugNode
from app.models.disease import DiseaseNode
from app.models.bpo import BpoNode
from app.models.mfn import MfnNode
from app.models.cco import CcoNode
from app.models.phenotype import PhenotypeNode
from app.models.anatomy import AnatomyNode
from app.models.pathway import PathwayNode
from app.models.exposure import ExposureNode
from app.models.edge import Edge

# Definición de Unión Discriminada para Nodos
# Esto permite que la API responda con el esquema exacto según el 'label'
StrictNode = Annotated[
    Union[
        GeneNode, 
        DrugNode, 
        DiseaseNode, 
        BpoNode, 
        MfnNode, 
        CcoNode, 
        PhenotypeNode, 
        AnatomyNode, 
        PathwayNode, 
        ExposureNode
    ],
    Field(discriminator='label')
]

class NodeResponse(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(..., description="Unique identifier for the node")
    label: str = Field(..., description="Biological label or category of the node")
    display_name: str = Field(..., description="Human-readable name for visualization")

class NeighborhoodResponse(BaseModel):
    node_id: str = Field(..., description="The ID of the queried central node")
    nodes: List[StrictNode] = Field(..., description="List of unique nodes in the neighborhood with full metadata")
    edges: List[Edge] = Field(..., description="List of edges connecting the nodes with full properties")

class RelationCount(BaseModel):
    relation: str = Field(..., description="Type of relationship")
    count: int = Field(..., description="Number of edges with this relation")

class NodeMetricsResponse(BaseModel):
    node_id: str = Field(..., description="The ID of the queried node")
    degree: int = Field(..., description="Total number of connections (edges)")
    relations_count: List[RelationCount] = Field(..., description="Breakdown of connections by relation type")

class SearchNodeResponse(BaseModel):
    items: List[StrictNode] = Field(..., description="List of nodes matching the search criteria")
    total: int = Field(..., description="Total number of matches")

class DiscoveryNodeResponse(BaseModel):
    items: List[StrictNode] = Field(..., description="List of nodes with full biological details")
    total: int = Field(..., description="Total number of matches found")

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
