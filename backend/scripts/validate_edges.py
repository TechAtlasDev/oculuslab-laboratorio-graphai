import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.models.edge import Edge
from app.services.optimus_service import OptimusService

def validate_edges_dataset(limit_per_relation: int = 200):
    service = OptimusService()
    print(f"--- Iniciando validación de aristas (Edges) ---")
    
    try:
        path_edges = service.get_file_path("edges.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de aristas: {e}")
        return

    # Obtener todas las relaciones únicas
    relations = (
        pl.scan_parquet(path_edges)
        .select("relation")
        .unique()
        .collect()["relation"]
        .to_list()
    )
    
    total_success = 0
    total_processed = 0
    errors = []

    for rel in relations:
        print(f"Validando relación: {rel}...")
        df_sample = (
            pl.scan_parquet(path_edges)
            .filter(pl.col("relation") == rel)
            .head(limit_per_relation)
            .collect()
        )
        
        for row in df_sample.to_dicts():
            total_processed += 1
            try:
                row_copy = row.copy()
                row_copy["properties"] = json.loads(row["properties"])
                Edge(**row_copy)
                total_success += 1
            except Exception as e:
                errors.append({
                    "relation": rel,
                    "from": row["from"],
                    "to": row["to"],
                    "error": str(e)
                })
                print(f"ERROR en {rel} ({row['from']} -> {row['to']}): {e}")
                break

    print("\n--- Resultados de la Validación de Aristas ---")
    print(f"Total procesadas: {total_processed}")
    print(f"Exitosas: {total_success}")
    print(f"Fallidas: {len(errors)}")
    
    if errors:
        print("\nEjemplo de error detectado:")
        print(json.dumps(errors[0], indent=2))
        sys.exit(1)
    else:
        print("\n¡Excelente! Las muestras de todas las relaciones cumplen con el esquema.")

if __name__ == "__main__":
    validate_edges_dataset(200)
