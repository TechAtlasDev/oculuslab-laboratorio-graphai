from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

class MockOptimusService:
    def get_node_neighborhood(self, node_id: str, limit: int = 15, relation: str | None = None, target_label: str | None = None):
        return {
            "node_id": node_id,
            "nodes": [
                {"id": node_id, "label": "Gene", "display_name": "EGFR"},
                {"id": "DRUG1", "label": "Drug", "display_name": "DRUG1"}
            ],
            "edges": [
                {"source": node_id, "target": "DRUG1", "relation": "TARGETS"}
            ]
        }

    def get_node_metrics(self, node_id: str):
        return {
            "node_id": node_id,
            "degree": 5,
            "relations_count": [{"relation": "EXPRESSION", "count": 5}]
        }

def test_get_node_neighborhood():
    # Override dependency
    from app.api.graph import get_optimus_service
    app.dependency_overrides[get_optimus_service] = MockOptimusService
    
    response = client.get("/api/v1/graph/nodes/ENSG00000146648/neighborhood?limit=15")
    
    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == "ENSG00000146648"
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1
    
    app.dependency_overrides.clear()

def test_search_nodes():
    # Override dependency
    from app.api.graph import get_optimus_service
    class MockSearchService:
        def search_nodes(self, query, label=None, limit=20):
            return {
                "items": [{"id": "ENSG1", "label": "GEN", "display_name": "ENSG1"}],
                "total": 1
            }
    app.dependency_overrides[get_optimus_service] = MockSearchService
    
    response = client.get("/api/v1/graph/nodes/search?q=EGFR")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == "ENSG1"
    
    app.dependency_overrides.clear()

def test_get_graph_stats():
    # Override dependency
    from app.api.graph import get_optimus_service
    class MockStatsService:
        def get_graph_stats(self):
            return {
                "total_nodes": 100,
                "total_edges": 500,
                "nodes_by_label": [{"label": "GEN", "count": 100}],
                "edges_by_relation": [{"relation": "INTERACTS", "count": 500}]
            }
    app.dependency_overrides[get_optimus_service] = MockStatsService
    
    response = client.get("/api/v1/graph/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_nodes"] == 100
    assert data["total_edges"] == 500
    
    app.dependency_overrides.clear()

def test_get_node_metrics():
    # Override dependency
    from app.api.graph import get_optimus_service
    app.dependency_overrides[get_optimus_service] = MockOptimusService
    
    response = client.get("/api/v1/graph/nodes/ENSG00000146648/metrics")
    
    assert response.status_code == 200
    data = response.json()
    assert data["node_id"] == "ENSG00000146648"
    assert data["degree"] == 5
    assert len(data["relations_count"]) == 1
    assert data["relations_count"][0]["relation"] == "EXPRESSION"
    
    app.dependency_overrides.clear()
