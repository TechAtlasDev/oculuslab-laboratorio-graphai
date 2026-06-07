from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_drug_repurposing_endpoint():
    # Override dependency
    from app.api.analysis import get_optimus_service
    class MockAnalysisService:
        def drug_repurposing_analysis(self, drug_id, limit=10):
            return {
                "drug_id": drug_id,
                "candidates": [
                    {
                        "disease": {"id": "DIS1", "label": "DIS", "display_name": "Disease 1"},
                        "intermediate_nodes": [{"id": "GEN1", "label": "GEN", "display_name": "Gene 1"}],
                        "evidence_count": 1
                    }
                ]
            }
    app.dependency_overrides[get_optimus_service] = MockAnalysisService
    
    response = client.get("/api/v1/analysis/repurpose/drug/CHEMBL1000")
    
    assert response.status_code == 200
    data = response.json()
    assert data["drug_id"] == "CHEMBL1000"
    assert len(data["candidates"]) == 1
    assert data["candidates"][0]["disease"]["id"] == "DIS1"
    
    app.dependency_overrides.clear()
