from fastapi import APIRouter, Depends, Query, Path
from app.models.graph import NeighborhoodResponse, NodeMetricsResponse
from app.services.optimus_service import OptimusService

router = APIRouter(prefix="/api/v1/graph", tags=["graph"])

def get_optimus_service():
    return OptimusService()

@router.get("/nodes/{node_id}/neighborhood", response_model=NeighborhoodResponse)
async def get_node_neighborhood(
    node_id: str = Path(..., description="ID of the node (e.g. ENSG00000146648)"),
    limit: int = Query(15, ge=1, le=100, description="Max number of connections to retrieve"),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Retrieve the 1-hop neighborhood for a given node.
    """
    data = service.get_node_neighborhood(node_id=node_id, limit=limit)
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
