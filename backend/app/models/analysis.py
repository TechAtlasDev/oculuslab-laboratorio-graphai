from pydantic import BaseModel, Field
from typing import List
from app.models.graph import NodeResponse

class RepurposeCandidate(BaseModel):
    disease: NodeResponse = Field(..., description="The potential disease target")
    intermediate_nodes: List[NodeResponse] = Field(..., description="Genes/Nodes connecting the drug to the disease")
    evidence_count: int = Field(..., description="Number of paths found between the drug and this disease")

class DrugRepurposeResponse(BaseModel):
    drug_id: str
    candidates: List[RepurposeCandidate] = Field(..., description="List of potential therapeutic uses found")
