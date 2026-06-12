import json
from fastapi.openapi.utils import get_openapi
import sys
from pathlib import Path

# Añadir el directorio raíz al path para poder importar la app
sys.path.append(str(Path(__file__).parent))

from app.app import app

def generate_frontend_docs():
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        openapi_version="3.1.0",
        description="Guía de integración para el Frontend - Laboratorio de Grafos",
        routes=app.routes,
    )

    doc_path = Path("docs/FRONTEND_API_GUIDE.md")
    
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(f"# 🧬 Guía de Integración API (v{app.version})\n\n")
        f.write("Esta documentación detalla los endpoints disponibles y las estructuras de datos estrictas para el frontend.\n\n")
        
        f.write("## 📌 Endpoints Principales\n\n")
        
        paths = openapi_schema.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                f.write(f"### `{method.upper()} {path}`\n")
                f.write(f"**Resumen:** {details.get('summary', 'Sin descripción')}\n\n")
                
                # Parámetros
                params = details.get("parameters", [])
                if params:
                    f.write("| Parámetro | Ubicación | Tipo | Requerido | Descripción |\n")
                    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
                    for p in params:
                        name = p.get("name")
                        in_ = p.get("in")
                        schema = p.get("schema", {})
                        type_ = schema.get("type", "mixed")
                        req = "✅" if p.get("required") else "❌"
                        desc = p.get("description", "-")
                        f.write(f"| `{name}` | `{in_}` | `{type_}` | {req} | {desc} |\n")
                    f.write("\n")

        f.write("## 🏗️ Modelos de Datos (Tipado Estricto)\n\n")
        f.write("El sistema usa **Uniones Discriminadas**. El campo `label` determina qué propiedades adicionales tendrá el objeto.\n\n")
        
        components = openapi_schema.get("components", {}).get("schemas", {})
        
        # Filtrar modelos relevantes para el frontend
        important_models = ["GeneProperties", "DrugProperties", "DiseaseProperties", "PharmacologicalProperties", "ClinicalProperties", "AssociationProperties"]
        
        for model_name in important_models:
            if model_name in components:
                model = components[model_name]
                f.write(f"### 📦 `{model_name}`\n")
                props = model.get("properties", {})
                if props:
                    f.write("| Propiedad | Tipo | Descripción |\n")
                    f.write("| :--- | :--- | :--- |\n")
                    for p_name, p_details in props.items():
                        p_type = p_details.get("type", "complex/any")
                        p_desc = p_details.get("description", "-")
                        f.write(f"| `{p_name}` | `{p_type}` | {p_desc} |\n")
                    f.write("\n")

    print(f"✅ Documentación generada en: {doc_path}")

if __name__ == "__main__":
    generate_frontend_docs()
