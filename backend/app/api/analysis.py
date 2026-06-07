from fastapi import APIRouter, Depends, Query, Path
from app.models.analysis import DrugRepurposeResponse
from app.services.optimus_service import OptimusService

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])

def get_optimus_service():
    return OptimusService()

@router.get("/repurpose/drug/{drug_id}", response_model=DrugRepurposeResponse)
async def drug_repurposing_analysis(
    drug_id: str = Path(..., description="ID of the drug to analyze (e.g. CHEMBL1000)"),
    limit: int = Query(10, ge=1, le=50),
    service: OptimusService = Depends(get_optimus_service)
):
    """
    Find potential new therapeutic uses for a drug (Drug -> Gene -> Disease).
    """
    data = service.drug_repurposing_analysis(drug_id=drug_id, limit=limit)
    return DrugRepurposeResponse(**data)
