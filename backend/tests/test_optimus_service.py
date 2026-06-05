import pytest
from unittest.mock import patch, MagicMock
from app.services.optimus_service import OptimusService

@pytest.fixture
def optimus_service():
    return OptimusService(cache_dir="/tmp/optimus_test_cache")

@patch('app.services.optimus_service.optimuskg')
def test_get_file_path(mock_optimuskg, optimus_service):
    mock_optimuskg.get_file.return_value = "/tmp/optimus_test_cache/nodes/gene.parquet"
    
    result = optimus_service.get_file_path("nodes/gene.parquet")
    
    assert result == "/tmp/optimus_test_cache/nodes/gene.parquet"
    mock_optimuskg.get_file.assert_called_once_with("nodes/gene.parquet")

@patch('app.services.optimus_service.optimuskg')
def test_load_nodes_and_edges(mock_optimuskg, optimus_service):
    mock_nodes = MagicMock()
    mock_edges = MagicMock()
    mock_optimuskg.load_graph.return_value = (mock_nodes, mock_edges)
    
    nodes, edges = optimus_service.load_nodes_and_edges(lcc=True)
    
    assert nodes == mock_nodes
    assert edges == mock_edges
    mock_optimuskg.load_graph.assert_called_once_with(lcc=True)

@patch('app.services.optimus_service.optimuskg')
def test_load_network_graph(mock_optimuskg, optimus_service):
    mock_graph = MagicMock()
    mock_optimuskg.load_networkx.return_value = mock_graph
    
    graph = optimus_service.load_network_graph(lcc=False)
    
    assert graph == mock_graph
    mock_optimuskg.load_networkx.assert_called_once_with(lcc=False)
