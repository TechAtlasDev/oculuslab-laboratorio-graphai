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

    def get_node_details(self, node_id: str) -> dict:
        """
        Retrieves full details for a specific node, including parsed properties.
        """
        import polars as pl
        import json
        
        logger.info(f"Fetching full details for node: {node_id}")
        path_nodes = self.get_file_path("nodes.parquet")
        
        lf_nodes = pl.scan_parquet(path_nodes)
        df_node = lf_nodes.filter(pl.col("id") == node_id).collect()
        
        if df_node.is_empty():
            raise ValueError(f"Node {node_id} not found")
            
        row = df_node.to_dicts()[0]
        props = {}
        if row["properties"]:
            try:
                props = json.loads(row["properties"])
            except:
                props = {"raw": row["properties"]}
                
        return {
            "id": row["id"],
            "label": row["label"],
            "display_name": row["id"].split("_")[-1],
            "properties": props
        }

    def get_node_neighborhood(self, node_id: str, limit: int = 15, relation: str | None = None, target_label: str | None = None) -> dict:
        """
        Retrieves the 1-hop neighborhood for a given node using Polars LazyFrames.
        Allows filtering by relation type and target node label.
        """
        import polars as pl
        
        logger.info(f"Fetching neighborhood for {node_id} with limit {limit}, relation={relation}, target_label={target_label}")
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        # Use LazyFrames
        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes).select(["id", "label"])

        # Filter edges where node_id is involved
        lf_filtered = lf_edges.filter(
            (pl.col("from") == node_id) | (pl.col("to") == node_id)
        )
        
        if relation:
            lf_filtered = lf_filtered.filter(pl.col("relation") == relation)

        # Join to get labels
        lf_with_from = lf_filtered.join(
            lf_nodes, left_on="from", right_on="id", how="left"
        ).rename({"label": "from_label"})

        lf_final = lf_with_from.join(
            lf_nodes, left_on="to", right_on="id", how="left"
        ).rename({"label": "to_label"})
        
        # Apply target label filtering
        if target_label:
            # The target node is the one that is NOT the node_id
            lf_final = lf_final.filter(
                ((pl.col("from") == node_id) & (pl.col("to_label") == target_label)) |
                ((pl.col("to") == node_id) & (pl.col("from_label") == target_label))
            )

        # Limit and collect
        try:
            df_result = lf_final.head(limit).collect()
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

    def get_node_metrics(self, node_id: str) -> dict:
        """
        Calculates basic metrics for a specific node, such as its degree and relations breakdown.
        """
        import polars as pl
        
        logger.info(f"Calculating metrics for node: {node_id}")
        path_edges = self.get_file_path("edges.parquet")
        
        lf_edges = pl.scan_parquet(path_edges)
        
        # Filter edges involving the node
        lf_node_edges = lf_edges.filter(
            (pl.col("from") == node_id) | (pl.col("to") == node_id)
        )
        
        try:
            # Aggregate relations count
            df_metrics = lf_node_edges.group_by("relation").agg(pl.len().alias("count")).collect()
            
            degree = df_metrics["count"].sum() if not df_metrics.is_empty() else 0
            relations_count = df_metrics.to_dicts()
            
            return {
                "node_id": node_id,
                "degree": degree,
                "relations_count": relations_count
            }
        except Exception as e:
            logger.error(f"Error executing polars query for metrics: {e}")
            raise

    def search_nodes(self, query: str, label: str | None = None, limit: int = 20) -> dict:
        """
        Search for nodes matching a query string in ID or properties.
        """
        import polars as pl
        
        logger.info(f"Searching nodes with query: {query}, label: {label}")
        path_nodes = self.get_file_path("nodes.parquet")
        lf_nodes = pl.scan_parquet(path_nodes)

        if label:
            lf_nodes = lf_nodes.filter(pl.col("label") == label)

        # Search in id or properties (case-insensitive)
        # Using regex search on the properties string
        lf_filtered = lf_nodes.filter(
            pl.col("id").str.contains(query, ignore_case=True) | 
            pl.col("properties").str.contains(query, ignore_case=True)
        ).head(limit)

        df_results = lf_filtered.collect()
        
        items = []
        for row in df_results.iter_rows(named=True):
            items.append({
                "id": row["id"],
                "label": row["label"],
                "display_name": row["id"].split("_")[-1]
            })
            
        return {
            "items": items,
            "total": len(items) # In a real scenario, we'd want a separate count query
        }

    def drug_repurposing_analysis(self, drug_id: str, limit: int = 10) -> dict:
        """
        Performs drug repurposing analysis (Drug -> Gen -> Disease).
        """
        import polars as pl
        
        logger.info(f"Starting drug repurposing analysis for: {drug_id}")
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes).select(["id", "label"])

        # 1. Find genes targeted by the drug
        lf_drug_edges = lf_edges.filter(
            (pl.col("from") == drug_id) | (pl.col("to") == drug_id)
        )
        
        # Get target IDs
        lf_targets = lf_drug_edges.select([
            pl.when(pl.col("from") == drug_id).then(pl.col("to")).otherwise(pl.col("from")).alias("target_id")
        ])
        
        # Filter only Genes (Joining only to check label, then dropping it)
        lf_target_genes = lf_targets.join(
            lf_nodes, left_on="target_id", right_on="id"
        ).filter(pl.col("label") == "GEN").select("target_id")

        # 2. Find diseases associated with these genes
        # Join target genes with edges to find connections
        # We only need the disease_id and the gene that got us there
        lf_gene_to_disease = lf_edges.join(
            lf_target_genes, left_on="from", right_on="target_id"
        ).select([
            pl.col("to").alias("disease_id"),
            pl.col("from").alias("target_id")
        ]).join(
            lf_nodes, left_on="disease_id", right_on="id"
        ).filter(pl.col("label") == "DIS").select(["disease_id", "target_id"])

        lf_gene_to_disease_rev = lf_edges.join(
            lf_target_genes, left_on="to", right_on="target_id"
        ).select([
            pl.col("from").alias("disease_id"),
            pl.col("to").alias("target_id")
        ]).join(
            lf_nodes, left_on="disease_id", right_on="id"
        ).filter(pl.col("label") == "DIS").select(["disease_id", "target_id"])

        # Combine results
        lf_candidates = pl.concat([
            lf_gene_to_disease.select(["disease_id", "target_id"]),
            lf_gene_to_disease_rev.select(["disease_id", "target_id"])
        ])

        # Group by disease to see which ones have more evidence
        df_analysis = lf_candidates.group_by("disease_id").agg([
            pl.col("target_id").unique().alias("intermediate_genes"),
            pl.len().alias("evidence_count")
        ]).sort("evidence_count", descending=True).head(limit).collect()

        # Build final response
        candidates = []
        for row in df_analysis.iter_rows(named=True):
            d_id = row["disease_id"]
            gene_ids = row["intermediate_genes"]
            
            candidates.append({
                "disease": {
                    "id": d_id,
                    "label": "DIS",
                    "display_name": d_id.split("_")[-1]
                },
                "intermediate_nodes": [
                    {"id": g, "label": "GEN", "display_name": g.split("_")[-1]} 
                    for g in gene_ids
                ],
                "evidence_count": row["evidence_count"]
            })

        return {
            "drug_id": drug_id,
            "candidates": candidates
        }

    def get_graph_stats(self) -> dict:
        """
        Get global statistics of the graph.
        """
        import polars as pl
        
        logger.info("Fetching global graph statistics")
        path_nodes = self.get_file_path("nodes.parquet")
        path_edges = self.get_file_path("edges.parquet")
        
        lf_nodes = pl.scan_parquet(path_nodes)
        lf_edges = pl.scan_parquet(path_edges)
        
        total_nodes = lf_nodes.select(pl.len()).collect().item()
        total_edges = lf_edges.select(pl.len()).collect().item()
        
        nodes_by_label = lf_nodes.group_by("label").agg(pl.len().alias("count")).collect().sort("count", descending=True).to_dicts()
        edges_by_relation = lf_edges.group_by("relation").agg(pl.len().alias("count")).collect().sort("count", descending=True).to_dicts()
        
        return {
            "total_nodes": total_nodes,
            "total_edges": total_edges,
            "nodes_by_label": nodes_by_label,
            "edges_by_relation": edges_by_relation
        }
