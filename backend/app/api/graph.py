from fastapi import APIRouter, Depends, Query, Path, HTTPException
from app.models.graph import (
    NeighborhoodResponse, 
    NodeMetricsResponse, 
    SearchNodeResponse, 
    GraphStatsResponse,
    StrictNode,
    DiscoveryNodeResponse
)
from app.services.optimus_service import OptimusService

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])

def get_optimus_service():
    return OptimusService()

@router.get("/discovery/nodes", response_model=DiscoveryNodeResponse)
async def discover_nodes(
    label: str | None = Query(None, description="Filter by node label (e.g. GEN, DRG)"),
    biotype: str | None = Query(None, description="Filter genes by biotype (e.g. protein_coding)"),
    chromosome: str | None = Query(None, description="Filter genes by chromosome (e.g. X, 1, 2)"),
    is_approved: bool | None = Query(None, description="Filter drugs by approval status"),
    max_phase: int | None = Query(None, ge=0, le=4, description="Filter drugs by max clinical phase"),
    therapeutic_area: str | None = Query(None, description="Filter diseases by therapeutic area"),
    limit: int = Query(20, ge=1, le=100),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Discovery endpoint to filter and find nodes based on advanced biological criteria.
    """
    data = service.discover_nodes(
        label=label, 
        biotype=biotype, 
        chromosome=chromosome, 
        is_approved=is_approved, 
        max_phase=max_phase,
        therapeutic_area=therapeutic_area,
        limit=limit
    )
    return DiscoveryNodeResponse(**data)

@router.get("/nodes/search", response_model=SearchNodeResponse)
async def search_nodes(
    q: str = Query(..., min_length=2, description="Search query (ID, symbol, or name)"),
    label: str | None = Query(None, description="Filter by node label (e.g. GEN, DRG)"),
    limit: int = Query(20, ge=1, le=100),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Search for nodes by ID or metadata properties.
    """
    data = service.search_nodes(query=q, label=label, limit=limit)
    return SearchNodeResponse(**data)

@router.get("/stats", response_model=GraphStatsResponse)
async def get_graph_stats(
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Get global graph statistics (counts, labels, relations).
    """
    data = service.get_graph_stats()
    return GraphStatsResponse(**data)

@router.get("/nodes/{node_id}", response_model=StrictNode)
async def get_node_details(
    node_id: str = Path(..., description="ID of the node to retrieve"),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Retrieve full details and metadata for a specific node.
    """
    try:
        data = service.get_node_details(node_id=node_id)
        return data
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/nodes/{node_id}/neighborhood", response_model=NeighborhoodResponse)
async def get_node_neighborhood(
    node_id: str = Path(..., description="ID of the node (e.g. ENSG00000146648)"),
    limit: int = Query(15, ge=1, le=100, description="Max number of connections to retrieve"),
    relation: str | None = Query(None, description="Filter by relation type"),
    target_label: str | None = Query(None, description="Filter by target node label"),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Retrieve the 1-hop neighborhood for a given node with optional filtering.
    """
    data = service.get_node_neighborhood(node_id=node_id, limit=limit, relation=relation, target_label=target_label)
    return NeighborhoodResponse(**data)

@router.get("/nodes/{node_id}/metrics", response_model=NodeMetricsResponse)
async def get_node_metrics(
    node_id: str = Path(..., description="ID of the node to analyze"),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Retrieve topological metrics for a specific node.
    """
    data = service.get_node_metrics(node_id=node_id)
    return NodeMetricsResponse(**data)
