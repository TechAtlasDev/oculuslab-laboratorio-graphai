import polars as pl
import json
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(str(Path(__file__).parent.parent))

from app.models.gene import GeneNode
from app.services.optimus_service import OptimusService

def validate_genes_dataset(limit: int = 1000):
    service = OptimusService()
    print(f"--- Iniciando validación de {limit} genes ---")
    
    try:
        path_nodes = service.get_file_path("nodes.parquet")
    except Exception as e:
        print(f"Error al obtener el archivo de nodos: {e}")
        return

    # Leer genes usando Polars
    lf_genes = pl.scan_parquet(path_nodes).filter(pl.col("label") == "GEN").head(limit)
    df_genes = lf_genes.collect()
    
    success_count = 0
    errors = []

    for i, row in enumerate(df_genes.to_dicts()):
        try:
            # Parsear las propiedades de JSON string a dict
            row_copy = row.copy()
            row_copy["properties"] = json.loads(row["properties"])
            
            # Validar con Pydantic
            GeneNode(**row_copy)
            success_count += 1
            
            if (i + 1) % 100 == 0:
                print(f"Procesados {i + 1} genes...")
                
        except Exception as e:
            errors.append({
                "id": row["id"],
                "error": str(e)
            })
            print(f"ERROR en gen {row['id']}: {e}")
            # Si hay un error de campo extra, queremos verlo de inmediato
            break 

    print("\n--- Resultados de la Validación ---")
    print(f"Total procesados: {len(df_genes)}")
    print(f"Exitosos: {success_count}")
    print(f"Fallidos: {len(errors)}")
    
    if errors:
        print("\nPrimer error detectado:")
        print(json.dumps(errors[0], indent=2))
        sys.exit(1)
    else:
        print("\n¡Felicidades! Todos los genes cumplen con el esquema estricto.")

if __name__ == "__main__":
    validate_genes_dataset(1000)
