import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import json
from app.app import app

client = TestClient(app)

@pytest.fixture
def mock_optimus_service():
    with patch('app.api.graph.OptimusService') as mock:
        yield mock.return_value

def test_discover_nodes_gen_filter(mock_optimus_service):
    # Setup mock return value
    mock_optimus_service.discover_nodes.return_value = {
        "items": [
            {
                "id": "ENSG00000000003",
                "label": "GEN",
                "display_name": "TSPAN6",
                "properties": {"biotype": "protein_coding", "symbol": "TSPAN6"}
            }
        ],
        "total": 1
    }
    
    response = client.get("/api/v1/graph/discovery/nodes?label=GEN&biotype=protein_coding")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["id"] == "ENSG00000000003"
    mock_optimus_service.discover_nodes.assert_called_once_with(
        label="GEN",
        biotype="protein_coding",
        chromosome=None,
        is_approved=None,
        max_phase=None,
        therapeutic_area=None,
        limit=20
    )

def test_discover_nodes_drg_filter(mock_optimus_service):
    # Setup mock return value
    mock_optimus_service.discover_nodes.return_value = {
        "items": [
            {
                "id": "CHEMBL1000",
                "label": "DRG",
                "display_name": "CETIRIZINE",
                "properties": {"is_approved": True, "maximum_clinical_trial_phase": 4}
            }
        ],
        "total": 1
    }
    
    response = client.get("/api/v1/graph/discovery/nodes?label=DRG&is_approved=true&max_phase=4")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["label"] == "DRG"
    mock_optimus_service.discover_nodes.assert_called_once_with(
        label="DRG",
        biotype=None,
        chromosome=None,
        is_approved=True,
        max_phase=4,
        therapeutic_area=None,
        limit=20
    )
