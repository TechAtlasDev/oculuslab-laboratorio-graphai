import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(str(Path(__file__).parent.parent))

from app.models.anatomy import AnatomyNode
from app.services.optimus_service import OptimusService

def validate_anatomy_dataset(limit: int = 1000):
    service = OptimusService()
    print(f"--- Iniciando validación de {limit} nodos de anatomía (ANA) ---")
    
    try:
        path_nodes = service.get_file_path("nodes.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de nodos: {e}")
        return

    # Leer ANA usando Polars
    lf_ana = pl.scan_parquet(path_nodes).filter(pl.col("label") == "ANA").head(limit)
    df_ana = lf_ana.collect()
    
    success_count = 0
    errors = []

    for i, row in enumerate(df_ana.to_dicts()):
        try:
            # Parsear las propiedades de JSON string a dict
            row_copy = row.copy()
            row_copy["properties"] = json.loads(row["properties"])
            
            # Validar con Pydantic
            AnatomyNode(**row_copy)
            success_count += 1
            
            if (i + 1) % 100 == 0:
                print(f"Procesados {i + 1} nodos ANA...")
                
        except Exception as e:
            errors.append({
                "id": row["id"],
                "error": str(e)
            })
            print(f"ERROR en nodo ANA {row['id']}: {e}")
            break 

    print("\n--- Resultados de la Validación ---")
    print(f"Total procesados: {len(df_ana)}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {len(errors)}")
    
    if errors:
        print("\nPrimer error detectado:")
        print(json.dumps(errors[0], indent=2))
        sys.exit(1)
    else:
        print("\n¡Felicidades! Todos los nodos de anatomía cumplen con el esquema estricto.")

if __name__ == "__main__":
    validate_anatomy_dataset(1000)
