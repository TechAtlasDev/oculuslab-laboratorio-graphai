import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(str(Path(__file__).parent.parent))

from app.models.exposure import ExposureNode
from app.services.optimus_service import OptimusService

def validate_exposure_dataset():
    service = OptimusService()
    print(f"--- Iniciando validación de nodos de exposición química (EXP) ---")
    
    try:
        path_nodes = service.get_file_path("nodes.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de nodos: {e}")
        return

    # Leer EXP usando Polars
    lf_exp = pl.scan_parquet(path_nodes).filter(pl.col("label") == "EXP")
    df_exp = lf_exp.collect()
    
    success_count = 0
    errors = []

    for i, row in enumerate(df_exp.to_dicts()):
        try:
            # Parsear las propiedades de JSON string a dict
            row_copy = row.copy()
            row_copy["properties"] = json.loads(row["properties"])
            
            # Validar con Pydantic
            ExposureNode(**row_copy)
            success_count += 1
            
            if (i + 1) % 200 == 0:
                print(f"Procesados {i + 1} nodos EXP...")
                
        except Exception as e:
            errors.append({
                "id": row["id"],
                "error": str(e)
            })
            print(f"ERROR en nodo EXP {row['id']}: {e}")
            break 

    print("\n--- Resultados de la Validación ---")
    print(f"Total procesados: {len(df_exp)}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {len(errors)}")
    
    if errors:
        print("\nPrimer error detectado:")
        print(json.dumps(errors[0], indent=2))
        sys.exit(1)
    else:
        print("\n¡Felicidades! Todos los nodos de exposición química cumplen con el esquema estricto.")

if __name__ == "__main__":
    validate_exposure_dataset()
