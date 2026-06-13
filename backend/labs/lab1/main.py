from app.services.optimus_service import OptimusService

optimuskg = OptimusService()
nodos = optimuskg.get_random_nodes(1000)

cluster_1 = []
cluster_2 = []

for nodo in nodos:
    if nodo["label"] == "GEN":
        cluster_1.append(nodo)
    
    if nodo["label"] == "DIS":
        cluster_2.append(nodo)

class Consultador:
    def __init__(self, cluster):
        self.cluster = cluster
        self.limite_capas = 10

    def consultar(self, capa):

        total_capas = len(self.cluster)
        elementos_por_capa = int(total_capas/self.limite_capas)
        
        inicio_capa = elementos_por_capa*(capa-1)
        fin_capa = elementos_por_capa*capa

        if inicio_capa >= total_capas:
            return 0
        
        if fin_capa >= total_capas:
            fin_capa = total_capas

        return self.cluster[inicio_capa:fin_capa]

Pepe = Consultador(cluster_1)
resultado = Pepe.consultar(capa=1)
print (len(resultado))
