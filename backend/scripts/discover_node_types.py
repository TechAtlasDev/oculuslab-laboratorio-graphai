import polars as pl
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.optimus_service import OptimusService

def identify_all_node_types():
    service = OptimusService()
    print("--- Iniciando descubrimiento de tipos de nodos ---")
    
    try:
        path_nodes = service.get_file_path("nodes.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de nodos: {e}")
        return

    # Escanear el dataset completo para encontrar valores únicos en la columna 'label'
    # Usamos scan_parquet para no cargar todo en memoria
    node_types = (
        pl.scan_parquet(path_nodes)
        .select("label")
        .unique()
        .collect()
    )
    
    labels = node_types["label"].to_list()
    print(f"\nSe han encontrado {len(labels)} tipos de nodos únicos:")
    for label in sorted(labels):
        # Contar cuántos nodos hay de cada tipo
        count = (
            pl.scan_parquet(path_nodes)
            .filter(pl.col("label") == label)
            .select(pl.len())
            .collect()
            .item()
        )
        print(f" - {label}: {count:,} nodos")

if __name__ == "__main__":
    identify_all_node_types()
