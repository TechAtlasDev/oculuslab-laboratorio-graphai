# Propuesta de Clustering basado en Machine Learning (Embeddings + t-SNE)

## 1. Concepto General
A diferencia del enfoque topológico (que agrupa nodos por sus conexiones o aristas directas), este enfoque agrupa los nodos basándose estrictamente en la **similitud de sus características intrínsecas (propiedades)**. Es altamente efectivo cuando queremos encontrar patrones ocultos en los metadatos de los nodos, independientemente de si están directamente conectados en el grafo.

## 2. Flujo de Trabajo (Pipeline)

### A. Extracción de Características (Feature Engineering)
El primer paso es extraer las propiedades relevantes de los nodos en formato JSON (por ejemplo: descripción, biotipo, área terapéutica, fases de pruebas clínicas) y normalizarlas.

### B. Vectorización (Embeddings)
Las características textuales o categóricas no pueden graficarse directamente. Se requiere convertir estos datos en **vectores matemáticos** (arreglos numéricos).
- Para textos descriptivos: Usar modelos de NLP (ej. `SentenceTransformers`, `TF-IDF`).
- Para datos categóricos: Usar `One-Hot Encoding`.
- Para datos topológicos integrados: Usar `Node2Vec` (que convierte la posición del nodo en el grafo en un vector).

El resultado será un vector de alta dimensionalidad (por ejemplo, 128 o 512 dimensiones) por cada nodo.

### C. Reducción de Dimensionalidad
Dado que es imposible visualizar 128 dimensiones en una pantalla, aplicamos algoritmos de reducción para comprimir esos vectores a exactamente **2 dimensiones (x, y)**.
- **UMAP (Uniform Manifold Approximation and Projection):** Excelente para preservar la estructura global y local de los datos. Muy rápido.
- **t-SNE (t-Distributed Stochastic Neighbor Embedding):** El estándar de la industria para visualizaciones 2D hermosas de datos complejos.

### D. Algoritmo de Clustering
Una vez que tenemos los puntos bidimensionales, aplicamos un algoritmo de aprendizaje no supervisado para agrupar los puntos cercanos:
- **K-Means:** Si tenemos una idea de cuántos clústeres queremos (agrupa por distancias euclidianas).
- **HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise):** Ideal si no sabemos cuántos clústeres hay y queremos identificar agrupaciones basadas en densidad, ignorando el ruido (outliers).

## 3. Librerías Necesarias (Stack Sugerido)
Para implementar este pipeline en Python, se requiere instalar:
```bash
uv add scikit-learn umap-learn matplotlib pandas
```

## 4. Ejemplo Conceptual de Código

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

# Supongamos que 'embeddings' es una matriz numpy de shape (N_nodos, 128)
# embeddings = obtener_vectores_de_nodos(nodos)

# 1. Reducir dimensiones a 2D (x, y)
tsne_model = TSNE(n_components=2, perplexity=30, random_state=42)
coordenadas_2d = tsne_model.fit_transform(embeddings)

# 2. Agrupar con K-Means (por ejemplo, buscando 5 clústeres)
kmeans = KMeans(n_clusters=5, random_state=42)
etiquetas_clusters = kmeans.fit_predict(coordenadas_2d)

# 3. Graficar
plt.figure(figsize=(10, 8))
scatter = plt.scatter(coordenadas_2d[:, 0], coordenadas_2d[:, 1], c=etiquetas_clusters, cmap='viridis', alpha=0.7)
plt.colorbar(scatter, label='Clúster ID')
plt.title("Clustering de Nodos usando t-SNE y K-Means")
plt.xlabel("Dimensión 1")
plt.ylabel("Dimensión 2")
plt.show()
```
