import json
import sys
from collections import defaultdict

def analyze_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    print("=== Análisis de la Estructura del JSON ===")
    print(f"Tipo raíz: {type(data).__name__}")
    
    if isinstance(data, dict):
        print("\nCampos principales:")
        for key, value in data.items():
            val_type = type(value).__name__
            
            if isinstance(value, list):
                length = len(value)
                if length > 0:
                    item_type = type(value[0]).__name__
                    print(f"- {key}: Lista de {length} elementos (Tipo de elemento: {item_type})")
                else:
                    print(f"- {key}: Lista vacía")
            elif isinstance(value, dict):
                print(f"- {key}: Objeto con {len(value)} claves")
                # Mostrar algunas subclaves
                subkeys = list(value.keys())[:5]
                print(f"    Subclaves de ejemplo: {', '.join(subkeys)}{'...' if len(value) > 5 else ''}")
            else:
                # Truncar valores largos de string
                str_val = str(value)
                if len(str_val) > 50:
                    str_val = str_val[:47] + "..."
                print(f"- {key}: {val_type} (Ejemplo: {str_val})")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_json(sys.argv[1])
    else:
        print("Por favor, proporciona la ruta al archivo JSON.")
