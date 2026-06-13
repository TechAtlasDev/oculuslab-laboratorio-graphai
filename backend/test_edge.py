from app.services.optimus_service import OptimusService

optimuskg = OptimusService()
data_edge = optimuskg.get_random_edge()
node_a = data_edge["from"]
node_b = data_edge["to"]
edges = optimuskg.get_edge_between_nodes(node_a, node_b)
print(f"Edges between {node_a} and {node_b}:")
print(edges)
