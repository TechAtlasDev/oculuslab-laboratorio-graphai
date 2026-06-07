import json
import polars as pl
from app.services.optimus_service import OptimusService

def test_real_discovery():
    service = OptimusService()
    drug_id = "CHEMBL1000" # Cetirizine
    
    print(f"--- Ejecutando análisis de reposicionamiento para: {drug_id} ---")
    
    try:
        results = service.drug_repurposing_analysis(drug_id, limit=5)
        
        print(f"\nDroga analizada: {results['drug_id']}")
        print(f"Candidatos encontrados: {len(results['candidates'])}")
        
        for i, candidate in enumerate(results['candidates'], 1):
            disease = candidate['disease']
            genes = [g['display_name'] for g in candidate['intermediate_nodes']]
            
            print(f"\n{i}. Enfermedad Candidata: {disease['display_name']} ({disease['id']})")
            print(f"   Genes Puente: {', '.join(genes)}")
            print(f"   Conteo de Evidencia: {candidate['evidence_count']}")
            
    except Exception as e:
        print(f"Error durante el análisis: {e}")

if __name__ == "__main__":
    test_real_discovery()
