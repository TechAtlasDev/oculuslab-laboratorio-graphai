import polars as pl
import json
from app.services.optimus_service import OptimusService

def inspect_datasets():
    service = OptimusService()
    
    files = ["nodes.parquet", "edges.parquet"]
    analysis = {}

    for file_name in files:
        print(f"--- Analyzing {file_name} ---")
        path = str(service.get_file_path(file_name))
        print(f"Path: {path}")
        
        lf = pl.scan_parquet(path)
        
        # Schema
        schema = {k: str(v) for k, v in lf.collect_schema().items()}
        print(f"Schema: {schema}")
        
        # Row count
        count = lf.select(pl.len()).collect().item()
        print(f"Row count: {count}")
        
        # Unique values for key columns
        unique_stats = {}
        if file_name == "nodes.parquet":
            unique_labels = lf.group_by("label").agg(pl.len().alias("count")).collect().sort("count", descending=True)
            unique_stats["labels"] = unique_labels.to_dicts()
            print("Top Labels:")
            print(unique_labels.head(10))
        elif file_name == "edges.parquet":
            unique_relations = lf.group_by("relation").agg(pl.len().alias("count")).collect().sort("count", descending=True)
            unique_stats["relations"] = unique_relations.to_dicts()
            print("Top Relations:")
            print(unique_relations.head(10))
            
        # Sample
        sample = lf.head(5).collect().to_dicts()
        
        analysis[file_name] = {
            "path": path,
            "schema": schema,
            "row_count": count,
            "unique_stats": unique_stats,
            "sample": sample
        }
        print("\n")

    with open("docs/dataset_analysis.json", "w") as f:
        json.dump(analysis, f, indent=4)
    print("Analysis saved to docs/dataset_analysis.json")

if __name__ == "__main__":
    inspect_datasets()
