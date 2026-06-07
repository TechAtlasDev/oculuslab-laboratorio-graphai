import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.optimus_service import OptimusService

def identify_all_edge_relations():
    service = OptimusService()
    print("--- Iniciando descubrimiento de tipos de relaciones (Edges) ---")
    
    try:
        path_edges = service.get_file_path("edges.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de aristas: {e}")
        return

    # Escanear el dataset de aristas para encontrar valores únicos en la columna 'relation'
    edge_types = (
        pl.scan_parquet(path_edges)
        .select("relation")
        .unique()
        .collect()
    )
    
    relations = edge_types["relation"].to_list()
    print(f"\nSe han encontrado {len(relations)} tipos de relaciones únicas:")
    
    for rel in sorted(relations):
        # Obtener el conteo y una muestra de propiedades
        sample = (
            pl.scan_parquet(path_edges)
            .filter(pl.col("relation") == rel)
            .head(1)
            .collect()
        )
        
        count = (
            pl.scan_parquet(path_edges)
            .filter(pl.col("relation") == rel)
            .select(pl.len())
            .collect()
            .item()
        )
        
        props_sample = sample["properties"].to_list()[0]
        print(f"\n - {rel}: {count:,} aristas")
        print(f"   Muestra Propiedades: {props_sample[:200]}...")

if __name__ == "__main__":
    identify_all_edge_relations()
