class Clusterizador():
    def __init__(self, cluster, num_capas=10):
        self.cluster = cluster
        self.num_capas = num_capas

    def consultar(self, num_capa:int):
        total_capas = len(self.cluster)
        elementos_por_capa = int(total_capas/self.num_capas)
        
        inicio_capa = elementos_por_capa*(num_capa-1)
        fin_capa = elementos_por_capa*num_capa

        if inicio_capa >= total_capas:
            return 0
        
        if fin_capa >= total_capas:
            fin_capa = total_capas

        return self.cluster[inicio_capa:fin_capa]
