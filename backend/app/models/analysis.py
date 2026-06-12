from pydantic import BaseModel, Field
from typing import List
from app.models.graph import StrictNode

class RepurposeCandidate(BaseModel):
    # En reposicionamiento forward, 'target' es una enfermedad. 
    # En inverso, 'target' es una droga.
    # Usamos StrictNode para que mantenga toda la metadata blindada.
    target: StrictNode = Field(..., description="The potential candidate (Drug if searching by Disease, or vice versa)")
    intermediate_nodes: List[StrictNode] = Field(..., description="Genes/Nodes connecting the source to the target")
    evidence_count: int = Field(..., description="Number of paths found")

class DrugRepurposeResponse(BaseModel):
    drug_id: str
    candidates: List[RepurposeCandidate] = Field(..., description="List of potential diseases found for this drug")

class DiseaseRepurposeResponse(BaseModel):
    disease_id: str
    candidates: List[RepurposeCandidate] = Field(..., description="List of potential drugs found for this disease")
