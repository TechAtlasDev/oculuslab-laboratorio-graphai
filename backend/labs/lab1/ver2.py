from app.services.clusterizador import Clusterizador
from app.services.optimus_service import OptimusService

optimuskg = OptimusService()
muestra_nodos = optimuskg.get_random_nodes(1000)

clusteres = {}

for nodo in muestra_nodos:
    if nodo["label"] not in clusteres:
        clusteres[nodo["label"]] = []
    clusteres[nodo["label"]].append(nodo)

clusterizador = Clusterizador(cluster=clusteres["GEN"], num_capas=100)
resultado = clusterizador.consultar(num_capa=1)

print (len(clusteres["GEN"]))
print (len(resultado))