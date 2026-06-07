import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(str(Path(__file__).parent.parent))

from app.models.pathway import PathwayNode
from app.services.optimus_service import OptimusService

def validate_pathway_dataset(limit: int = 10000):
    service = OptimusService()
    print(f"--- Iniciando validación de nodos de rutas metabólicas (PWY) ---")
    
    try:
        path_nodes = service.get_file_path("nodes.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de nodos: {e}")
        return

    # Leer PWY usando Polars
    lf_pwy = pl.scan_parquet(path_nodes).filter(pl.col("label") == "PWY").head(limit)
    df_pwy = lf_pwy.collect()
    
    success_count = 0
    errors = []

    for i, row in enumerate(df_pwy.to_dicts()):
        try:
            # Parsear las propiedades de JSON string a dict
            row_copy = row.copy()
            row_copy["properties"] = json.loads(row["properties"])
            
            # Validar con Pydantic
            PathwayNode(**row_copy)
            success_count += 1
            
            if (i + 1) % 500 == 0:
                print(f"Procesados {i + 1} nodos PWY...")
                
        except Exception as e:
            errors.append({
                "id": row["id"],
                "error": str(e)
            })
            print(f"ERROR en nodo PWY {row['id']}: {e}")
            break 

    print("\n--- Resultados de la Validación ---")
    print(f"Total procesados: {len(df_pwy)}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {len(errors)}")
    
    if errors:
        print("\nPrimer error detectado:")
        print(json.dumps(errors[0], indent=2))
        sys.exit(1)
    else:
        print("\n¡Felicidades! Todas las rutas metabólicas cumplen con el esquema estricto.")

if __name__ == "__main__":
    validate_pathway_dataset()
