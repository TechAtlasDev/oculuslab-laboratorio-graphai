import logging
import optimuskg
import polars as pl
import json

logger = logging.getLogger(__name__)

class OptimusService:
    def __init__(self, cache_dir: str | None = None):
        if cache_dir:
            optimuskg.set_cache_dir(cache_dir)
            logger.info(f"Set OptimusKG cache dir to: {cache_dir}")
            
    def get_file_path(self, path: str) -> str:
        return optimuskg.get_file(path)
        
    def get_node_details(self, node_id: str) -> dict:
        path_nodes = self.get_file_path("nodes.parquet")
        lf_nodes = pl.scan_parquet(path_nodes)
        df_node = lf_nodes.filter(pl.col("id") == node_id).collect()
        
        if df_node.is_empty():
            raise ValueError(f"Node {node_id} not found")
            
        row = df_node.to_dicts()[0]
        return {
            "id": row["id"],
            "label": row["label"],
            "display_name": row["id"].split("_")[-1],
            "properties": json.loads(row["properties"]) if row["properties"] else {}
        }

    def get_node_neighborhood(self, node_id: str, limit: int = 15, relation: str | None = None, target_label: str | None = None) -> dict:
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes)

        # 1. Buscar aristas conectadas
        lf_filtered = lf_edges.filter((pl.col("from") == node_id) | (pl.col("to") == node_id))
        if relation:
            lf_filtered = lf_filtered.filter(pl.col("relation") == relation)
        
        df_edges_raw = lf_filtered.head(limit).collect()
        
        # 2. Recolectar todos los IDs de nodos involucrados (central + vecinos)
        connected_ids = set()
        for row in df_edges_raw.iter_rows(named=True):
            connected_ids.add(row["from"])
            connected_ids.add(row["to"])
        connected_ids.add(node_id)

        # 3. Obtener metadatos completos de esos nodos
        df_nodes_data = lf_nodes.filter(pl.col("id").is_in(list(connected_ids))).collect()
        
        nodes_map = {}
        for row in df_nodes_data.to_dicts():
            nodes_map[row["id"]] = {
                "id": row["id"],
                "label": row["label"],
                "display_name": row["id"].split("_")[-1],
                "properties": json.loads(row["properties"]) if row["properties"] else {}
            }

        # 4. Formatear aristas según el modelo estricto
        formatted_edges = []
        for row in df_edges_raw.to_dicts():
            formatted_edges.append({
                "from": row["from"],
                "to": row["to"],
                "relation": row["relation"],
                "label": row["label"],
                "undirected": row["undirected"],
                "properties": json.loads(row["properties"]) if row["properties"] else {}
            })

        return {
            "node_id": node_id,
            "nodes": list(nodes_map.values()),
            "edges": formatted_edges
        }

    def search_nodes(self, query: str, label: str | None = None, limit: int = 20) -> dict:
        path_nodes = self.get_file_path("nodes.parquet")
        lf_nodes = pl.scan_parquet(path_nodes)

        if label:
            lf_nodes = lf_nodes.filter(pl.col("label") == label)

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
                "display_name": row["id"].split("_")[-1],
                "properties": json.loads(row["properties"]) if row["properties"] else {}
            })
            
        return {
            "items": items,
            "total": len(items)
        }

    def discover_nodes(self, label: str | None = None, biotype: str | None = None, chromosome: str | None = None,
                       is_approved: bool | None = None, max_phase: int | None = None,
                       therapeutic_area: str | None = None, limit: int = 20) -> dict:
        path_nodes = self.get_file_path("nodes.parquet")
        lf_nodes = pl.scan_parquet(path_nodes)

        if label:
            lf_nodes = lf_nodes.filter(pl.col("label") == label)

        if biotype or chromosome or is_approved is not None or max_phase is not None or therapeutic_area:
            properties_schema = pl.Struct([
                pl.Field("biotype", pl.String),
                pl.Field("is_approved", pl.Boolean),
                pl.Field("maximum_clinical_trial_phase", pl.Float64),
                pl.Field("therapeutic_areas", pl.List(pl.String)),
                pl.Field("canonical_transcript", pl.Struct([pl.Field("chromosome", pl.String)])),
                pl.Field("genomic_location", pl.Struct([pl.Field("chromosome", pl.String)])),
            ])

            lf_nodes = lf_nodes.with_columns(
                pl.col("properties").str.json_decode(dtype=properties_schema).alias("parsed_props")
            )

            if biotype:
                lf_nodes = lf_nodes.filter(pl.col("parsed_props").struct.field("biotype") == biotype)
            if chromosome:
                lf_nodes = lf_nodes.filter(
                    (pl.col("parsed_props").struct.field("canonical_transcript").struct.field("chromosome") == chromosome) |
                    (pl.col("parsed_props").struct.field("genomic_location").struct.field("chromosome") == chromosome)
                )
            if is_approved is not None:
                lf_nodes = lf_nodes.filter(pl.col("parsed_props").struct.field("is_approved") == is_approved)
            if max_phase is not None:
                lf_nodes = lf_nodes.filter(pl.col("parsed_props").struct.field("maximum_clinical_trial_phase") == float(max_phase))
            if therapeutic_area:
                lf_nodes = lf_nodes.filter(pl.col("parsed_props").struct.field("therapeutic_areas").list.contains(therapeutic_area))

        df_results = lf_nodes.head(limit).collect()
        
        items = []
        for row in df_results.iter_rows(named=True):
            items.append({
                "id": row["id"],
                "label": row["label"],
                "display_name": row["id"].split("_")[-1],
                "properties": json.loads(row["properties"]) if row["properties"] else {}
            })
            
        return {"items": items, "total": len(items)}

    def drug_repurposing_analysis(self, drug_id: str, limit: int = 10) -> dict:
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes)

        # 1. Genes diana
        lf_drug_edges = lf_edges.filter((pl.col("from") == drug_id) | (pl.col("to") == drug_id))
        lf_targets = lf_drug_edges.select([
            pl.when(pl.col("from") == drug_id).then(pl.col("to")).otherwise(pl.col("from")).alias("target_id")
        ])
        lf_target_genes = lf_targets.join(lf_nodes.select(["id", "label"]), left_on="target_id", right_on="id").filter(pl.col("label") == "GEN").select("target_id")

        # 2. Enfermedades asociadas
        lf_gene_to_disease = lf_edges.join(lf_target_genes, left_on="from", right_on="target_id").select([pl.col("to").alias("disease_id"), pl.col("from").alias("target_id")])
        lf_gene_to_disease_rev = lf_edges.join(lf_target_genes, left_on="to", right_on="target_id").select([pl.col("from").alias("disease_id"), pl.col("to").alias("target_id")])
        lf_candidates_ids = pl.concat([lf_gene_to_disease, lf_gene_to_disease_rev])

        df_analysis = lf_candidates_ids.group_by("disease_id").agg([
            pl.col("target_id").unique().alias("intermediate_genes"),
            pl.len().alias("evidence_count")
        ]).sort("evidence_count", descending=True).head(limit).collect()

        # 3. Obtener metadatos completos para la respuesta estricta
        all_node_ids = set()
        for row in df_analysis.iter_rows(named=True):
            all_node_ids.add(row["disease_id"])
            for g in row["intermediate_genes"]:
                all_node_ids.add(g)
        
        df_meta = lf_nodes.filter(pl.col("id").is_in(list(all_node_ids))).collect()
        meta_map = {r["id"]: {
            "id": r["id"], "label": r["label"], "display_name": r["id"].split("_")[-1], 
            "properties": json.loads(r["properties"]) if r["properties"] else {}
        } for r in df_meta.to_dicts()}

        candidates = []
        for row in df_analysis.iter_rows(named=True):
            candidates.append({
                "target": meta_map[row["disease_id"]],
                "intermediate_nodes": [meta_map[g] for g in row["intermediate_genes"]],
                "evidence_count": row["evidence_count"]
            })

        return {"drug_id": drug_id, "candidates": candidates}

    def disease_repurposing_analysis(self, disease_id: str, limit: int = 10) -> dict:
        """
        Performs inverse drug repurposing analysis (Disease -> Gen -> Drug).
        """
        import polars as pl
        import json
        
        path_edges = self.get_file_path("edges.parquet")
        path_nodes = self.get_file_path("nodes.parquet")

        lf_edges = pl.scan_parquet(path_edges)
        lf_nodes = pl.scan_parquet(path_nodes)

        # 1. Genes asociados a la enfermedad (DIS -> GEN)
        lf_disease_edges = lf_edges.filter((pl.col("from") == disease_id) | (pl.col("to") == disease_id))
        lf_targets = lf_disease_edges.select([
            pl.when(pl.col("from") == disease_id).then(pl.col("to")).otherwise(pl.col("from")).alias("target_id")
        ])
        lf_associated_genes = lf_targets.join(
            lf_nodes.select(["id", "label"]), left_on="target_id", right_on="id"
        ).filter(pl.col("label") == "GEN").select("target_id")

        # 2. Drogas que atacan estos genes (GEN -> DRG)
        lf_gene_to_drug = lf_edges.join(
            lf_associated_genes, left_on="from", right_on="target_id"
        ).select([pl.col("to").alias("drug_id"), pl.col("from").alias("target_id")])
        
        lf_gene_to_drug_rev = lf_edges.join(
            lf_associated_genes, left_on="to", right_on="target_id"
        ).select([pl.col("from").alias("drug_id"), pl.col("to").alias("target_id")])
        
        lf_candidates_ids = pl.concat([lf_gene_to_drug, lf_gene_to_drug_rev]).join(
            lf_nodes.select(["id", "label"]), left_on="drug_id", right_on="id"
        ).filter(pl.col("label") == "DRG").select(["drug_id", "target_id"])

        df_analysis = lf_candidates_ids.group_by("drug_id").agg([
            pl.col("target_id").unique().alias("intermediate_genes"),
            pl.len().alias("evidence_count")
        ]).sort("evidence_count", descending=True).head(limit).collect()

        # 3. Obtener metadatos completos
        all_node_ids = set()
        for row in df_analysis.iter_rows(named=True):
            all_node_ids.add(row["drug_id"])
            for g in row["intermediate_genes"]:
                all_node_ids.add(g)
        
        df_meta = lf_nodes.filter(pl.col("id").is_in(list(all_node_ids))).collect()
        meta_map = {r["id"]: {
            "id": r["id"], "label": r["label"], "display_name": r["id"].split("_")[-1], 
            "properties": json.loads(r["properties"]) if r["properties"] else {}
        } for r in df_meta.to_dicts()}

        candidates = []
        for row in df_analysis.iter_rows(named=True):
            candidates.append({
                "target": meta_map[row["drug_id"]],
                "intermediate_nodes": [meta_map[g] for g in row["intermediate_genes"]],
                "evidence_count": row["evidence_count"]
            })

        return {"disease_id": disease_id, "candidates": candidates}

    def get_node_metrics(self, node_id: str) -> dict:
        path_edges = self.get_file_path("edges.parquet")
        lf_edges = pl.scan_parquet(path_edges)
        lf_node_edges = lf_edges.filter((pl.col("from") == node_id) | (pl.col("to") == node_id))
        df_metrics = lf_node_edges.group_by("relation").agg(pl.len().alias("count")).collect()
        degree = df_metrics["count"].sum() if not df_metrics.is_empty() else 0
        return {"node_id": node_id, "degree": degree, "relations_count": df_metrics.to_dicts()}

    def get_graph_stats(self) -> dict:
        path_nodes = self.get_file_path("nodes.parquet")
        path_edges = self.get_file_path("edges.parquet")
        lf_nodes = pl.scan_parquet(path_nodes)
        lf_edges = pl.scan_parquet(path_edges)
        return {
            "total_nodes": lf_nodes.select(pl.len()).collect().item(),
            "total_edges": lf_edges.select(pl.len()).collect().item(),
            "nodes_by_label": lf_nodes.group_by("label").agg(pl.len().alias("count")).collect().sort("count", descending=True).to_dicts(),
            "edges_by_relation": lf_edges.group_by("relation").agg(pl.len().alias("count")).collect().sort("count", descending=True).to_dicts()
        }
