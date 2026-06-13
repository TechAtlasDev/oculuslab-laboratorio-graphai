import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community as nx_comm
from app.services.optimus_service import OptimusService

def run_topological_clustering():
    print("Iniciando clustering topológico...")
    
    # 1. Obtener datos
    optimuskg = OptimusService()
    print("Obteniendo muestra de aristas (conexiones)...")
    # Usamos aristas porque necesitamos conexiones reales para armar el grafo topológico
    edges_data = optimuskg.get_random_edges(6000) 
    
    # 2. Construir el grafo de NetworkX
    G = nx.Graph()
    for edge in edges_data:
        G.add_edge(edge["from"], edge["to"], label=edge.get("relation", ""))
        
    print(f"Grafo construido con {G.number_of_nodes()} nodos y {G.number_of_edges()} aristas.")
    
    if G.number_of_edges() == 0:
        print("No se encontraron aristas suficientes para realizar el clustering.")
        return

    # Extraer el componente conectado más grande para una mejor visualización (opcional pero recomendado)
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    largest_component = G.subgraph(components[0])
    
    print(f"Componente principal tiene {largest_component.number_of_nodes()} nodos.")

    # 3. Aplicar Clustering (Detección de Comunidades - Louvain)
    # Louvain agrupa nodos fuertemente interconectados
    print("Calculando comunidades usando el algoritmo de Louvain...")
    communities = nx_comm.louvain_communities(largest_component)
    print(f"Se encontraron {len(communities)} comunidades (clústeres).")
    
    # Asignar un ID de clúster a cada nodo para colorearlo
    node_colors = []
    color_map = {}
    for cluster_id, community in enumerate(communities):
        for node in community:
            color_map[node] = cluster_id
            
    for node in largest_component.nodes():
        node_colors.append(color_map[node])
        
    # 4. Generar Coordenadas (Layout 2D)
    print("Calculando coordenadas 2D usando Spring Layout...")
    pos = nx.spring_layout(largest_component, seed=42)
    
    # 5. Visualizar
    plt.figure(figsize=(12, 10))
    nx.draw_networkx_nodes(largest_component, pos, node_size=50, node_color=node_colors, cmap=plt.cm.jet, alpha=0.8)
    nx.draw_networkx_edges(largest_component, pos, alpha=0.2)
    
    plt.title("Clustering Topológico de Nodos (Comunidades de Louvain)", fontsize=16)
    plt.axis("off")
    
    # Guardamos la imagen en lugar de plt.show() para evitar bloqueos en el entorno
    output_file = "labs/lab1/topological_clusters.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Visualización guardada exitosamente en: {output_file}")

if __name__ == "__main__":
    run_topological_clustering()
