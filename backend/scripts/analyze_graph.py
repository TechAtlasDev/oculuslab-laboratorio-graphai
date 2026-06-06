import polars as pl
import argparse
from app.services.optimus_service import OptimusService

def analyze_graph(top_k: int = 10):
    """
    Analyzes the graph to find the top K nodes with the highest degree.
    """
    print(f"Starting graph analysis to find top {top_k} hubs...")
    service = OptimusService()
    
    path_edges = service.get_file_path("edges.parquet")
    path_nodes = service.get_file_path("nodes.parquet")
    
    # Lazy scan
    lf_edges = pl.scan_parquet(path_edges)
    lf_nodes = pl.scan_parquet(path_nodes).select(["id", "label"])
    
    # Calculate degrees for 'from' nodes
    out_degree = lf_edges.group_by("from").agg(pl.len().alias("out_degree")).rename({"from": "node_id"})
    
    # Calculate degrees for 'to' nodes
    in_degree = lf_edges.group_by("to").agg(pl.len().alias("in_degree")).rename({"to": "node_id"})
    
    # Join and calculate total degree
    # We use full outer join using polars syntax: how="full" or coalescing
    # Since outer join in LazyFrame might be restrictive, let's concat and group by
    all_nodes = pl.concat([
        lf_edges.select(pl.col("from").alias("node_id")),
        lf_edges.select(pl.col("to").alias("node_id"))
    ])
    
    df_degree = all_nodes.group_by("node_id").agg(pl.len().alias("degree")).collect()
    
    # Sort and get top K
    df_top = df_degree.sort("degree", descending=True).head(top_k)
    
    # Join with node labels
    df_labels = pl.read_parquet(path_nodes, columns=["id", "label"])
    
    df_final = df_top.join(df_labels, left_on="node_id", right_on="id", how="left")
    
    print("\n=== TOP HUB NODES ===")
    print(df_final)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze graph nodes")
    parser.add_argument("--top", type=int, default=10, help="Number of top nodes to display")
    args = parser.parse_args()
    
    analyze_graph(args.top)
