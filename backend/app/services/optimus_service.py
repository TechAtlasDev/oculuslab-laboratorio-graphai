import logging
import optimuskg

logger = logging.getLogger(__name__)

class OptimusService:
    def __init__(self, cache_dir: str | None = None):
        """
        Initialize the OptimusService.
        Allows passing a custom cache_dir (e.g. for testing)
        """
        if cache_dir:
            optimuskg.set_cache_dir(cache_dir)
            logger.info(f"Set OptimusKG cache dir to: {cache_dir}")
            
    def get_file_path(self, path: str) -> str:
        """
        Fetch a specific file and get its local path.
        """
        return optimuskg.get_file(path)
        
    def load_nodes_and_edges(self, lcc: bool = True):
        """
        Loads the nodes and edges of the graph as Polars DataFrames.
        """
        logger.info(f"Loading nodes and edges (LCC: {lcc})")
        nodes, edges = optimuskg.load_graph(lcc=lcc)
        return nodes, edges

    def load_network_graph(self, lcc: bool = True):
        """
        Loads the graph as a NetworkX MultiDiGraph.
        """
        logger.info(f"Loading NetworkX graph (LCC: {lcc})")
        return optimuskg.load_networkx(lcc=lcc)

    def get_node_neighborhood(self, node_id: str, limit: int = 15) -> dict:
        """
        Retrieves the 1-hop neighborhood for a given node using Polars LazyFrames.
        """
        import polars as pl
        
        logger.info(f"Fetching neighborhood for {node_id} with limit {limit}")
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        # Use LazyFrames for memory efficiency and speed
        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes).select(["id", "label"])

        # Filter edges where node_id is either 'from' or 'to'
        lf_filtered = lf_edges.filter(
            (pl.col("from") == node_id) | (pl.col("to") == node_id)
        ).head(limit)

        # Join to get 'from' node labels
        lf_with_from = lf_filtered.join(
            lf_nodes, left_on="from", right_on="id", how="left"
        ).rename({"label": "from_label"})

        # Join to get 'to' node labels
        lf_final = lf_with_from.join(
            lf_nodes, left_on="to", right_on="id", how="left"
        ).rename({"label": "to_label"})

        # Execute query
        try:
            df_result = lf_final.collect()
        except Exception as e:
            logger.error(f"Error executing polars query: {e}")
            raise

        edges = []
        unique_nodes = {}

        for row in df_result.iter_rows(named=True):
            f_id = row["from"]
            t_id = row["to"]
            relation = row["relation"]
            f_label = row.get("from_label") or "Unknown"
            t_label = row.get("to_label") or "Unknown"

            edges.append({
                "source": f_id,
                "target": t_id,
                "relation": relation
            })

            # Process nodes to maintain a unique list
            if f_id not in unique_nodes:
                unique_nodes[f_id] = {
                    "id": f_id,
                    "label": f_label,
                    "display_name": f_id.split("_")[-1]
                }
            if t_id not in unique_nodes:
                unique_nodes[t_id] = {
                    "id": t_id,
                    "label": t_label,
                    "display_name": t_id.split("_")[-1]
                }

        return {
            "node_id": node_id,
            "nodes": list(unique_nodes.values()),
            "edges": edges
        }
