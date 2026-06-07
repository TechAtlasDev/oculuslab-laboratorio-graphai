import polars as pl
import json
from app.services.optimus_service import OptimusService

def analyze_node_properties():
    service = OptimusService()
    path_nodes = service.get_file_path("nodes.parquet")
    
    # Load nodes
    lf_nodes = pl.scan_parquet(path_nodes)
    
    # Get unique labels to iterate
    labels = lf_nodes.select("label").unique().collect()["label"].to_list()
    print(f"Found labels: {labels}")
    
    metadata_summary = {}

    for label in labels:
        print(f"Analyzing metadata for label: {label}")
        # Get a few samples for this label
        samples = lf_nodes.filter(pl.col("label") == label).head(3).collect()
        
        label_samples = []
        for row in samples.iter_rows(named=True):
            props_str = row.get("properties")
            props = {}
            if props_str:
                try:
                    props = json.loads(props_str)
                except Exception as e:
                    props = {"error": f"Failed to parse JSON: {e}", "raw": props_str}
            
            label_samples.append({
                "id": row["id"],
                "properties": props
            })
        
        # Identify common keys in properties for this label
        all_keys = set()
        for s in label_samples:
            all_keys.update(s["properties"].keys())
            
        metadata_summary[label] = {
            "common_keys": list(all_keys),
            "samples": label_samples
        }

    with open("docs/node_metadata_analysis.json", "w") as f:
        json.dump(metadata_summary, f, indent=4)
        
    print("\n=== METADATA SUMMARY PER LABEL ===")
    for label, info in metadata_summary.items():
        print(f"\nLabel: {label}")
        print(f"Available keys: {info['common_keys']}")
        if info['samples']:
            print(f"Example ID: {info['samples'][0]['id']}")
            # Print a snippet of the first sample's properties
            first_props = info['samples'][0]['properties']
            snippet = {k: first_props[k] for k in list(first_props.keys())[:5]}
            print(f"Sample properties snippet: {snippet}")

if __name__ == "__main__":
    analyze_node_properties()
