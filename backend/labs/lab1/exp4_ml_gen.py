import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from app.services.optimus_service import OptimusService

def run_ml_clustering_gen():
    print("Iniciando clustering de Machine Learning para nodos GEN...")
    
    # 1. Obtener datos (todos los nodos GEN)
    import polars as pl
    optimuskg = OptimusService()
    print("Obteniendo TODOS los nodos de tipo GEN desde la base de datos...")
    path_nodes = optimuskg.get_file_path("nodes.parquet")
    df_nodes = pl.read_parquet(path_nodes)
    gen_nodes = df_nodes.filter(pl.col("label") == "GEN").to_dicts()
    
    print(f"Se filtraron {len(gen_nodes)} nodos de tipo GEN para analizar.")
    
    if len(gen_nodes) < 10:
        print("No hay suficientes nodos GEN en la muestra para hacer clustering.")
        return

    # 2. Extracción de Características (Feature Engineering)
    # Anteriormente colapsaron porque muchos genes tenían los mismos textos exactos.
    # Ahora usaremos el biotipo (categórico) y el transcription_start_site (numérico continuo)
    # para que los puntos se dispersen de manera realista.
    features_list = []
    valid_nodes = []
    
    for n in gen_nodes:
        import json
        props = n.get("properties") or {}
        if isinstance(props, str):
            try:
                props = json.loads(props)
            except:
                props = {}
                
        biotype = props.get("biotype", "unknown") or "unknown"
        tss = props.get("transcription_start_site", 0) or 0
        
        try:
            tss = float(tss)
            features_list.append({"biotype": biotype, "tss": tss})
            valid_nodes.append(n)
        except ValueError:
            pass

    print(f"{len(valid_nodes)} nodos GEN procesados.")

    # 3. Vectorización y Escalado
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.preprocessing import StandardScaler
    
    print("Vectorizando propiedades...")
    vectorizer = DictVectorizer(sparse=False)
    X_vectors_raw = vectorizer.fit_transform(features_list)
    
    # Es crucial escalar los datos cuando mezclamos continuos con categóricos
    scaler = StandardScaler()
    X_vectors = scaler.fit_transform(X_vectors_raw)

    # 4. Clustering (K-Means)
    n_clusters = 5
    print(f"Agrupando los nodos en {n_clusters} clústeres usando K-Means...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    cluster_labels = kmeans.fit_predict(X_vectors)

    # 5. Reducción de Dimensionalidad para Visualización (UMAP)
    # UMAP creará "islas" o nubes orgánicas a partir de las propiedades.
    print("Reduciendo dimensiones a 2D usando UMAP para generar gráficos orgánicos...")
    import umap
    reducer = umap.UMAP(n_components=2, random_state=42, n_neighbors=30, min_dist=0.2, init='random')
    coords_2d = reducer.fit_transform(X_vectors)

    # 6. Visualización
    plt.figure(figsize=(12, 10))
    
    # Graficar los puntos (cada color es un cluster)
    scatter = plt.scatter(coords_2d[:, 0], coords_2d[:, 1], c=cluster_labels, cmap='viridis', alpha=0.3, s=20)
    
    # Añadir leyenda de colores
    plt.colorbar(scatter, label='Clúster Asignado por K-Means')
    
    plt.title("Clustering Biológico para Nodos GEN (K-Means + UMAP)", fontsize=16)
    plt.xlabel("Dimensión UMAP 1")
    plt.ylabel("Dimensión UMAP 2")
    
    # Guardar gráfica
    output_file = "labs/lab1/ml_gen_clusters.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Visualización guardada exitosamente en: {output_file}")

if __name__ == "__main__":
    run_ml_clustering_gen()
