import numpy as np
import os
import shutil
import threading
import graphviz
from make_landscape import Landscape

class EvolucionDirigida(Landscape):
    def __init__(self, seq, g, p, output):
        self.seq = seq
        self.g = g
        self.p = p
        self.output = output
        self.dot = graphviz.Digraph()
        self.edges = []
        super().__init__()
    
    def main(self):
        # Creamos una carpeta para exportar los resultados
        ruta_resultados = os.path.join(self.output, 'results')
        if os.path.isdir(ruta_resultados):
            shutil.rmtree(ruta_resultados)
        os.mkdir(ruta_resultados)
        
        # Tiempo 0
        if self.g >= 0:
            t = threading.Thread(self.generaciones(secuencia=self.seq, tiempo=0, ruta=ruta_resultados))
            t.start()

            self.generar_data_grafo(ruta=ruta_resultados, tiempo=1)
    
    def generaciones(self, secuencia, tiempo, ruta):
        landscape_original = self.generar_landscape_original(secuencia=secuencia, tiempo=tiempo, ruta=ruta)

        if tiempo == 0:
            if self.g >= 1:
                ruta_generacion = self.crear_directorio_generacion(ruta=ruta, tiempo=1)
                landscape_filtrado = self.filtrar_landscape(data=landscape_original, tiempo=1, ruta=ruta_generacion)

                self.recorrer_secuencias(data=landscape_filtrado, tiempo=1, ruta=ruta_generacion)
        elif tiempo >= 1:
            if tiempo + 1 <= self.g:
                ruta_generacion = self.crear_directorio_generacion(ruta=ruta, tiempo=tiempo+1)

                landscape_filtrado = self.filtrar_landscape(data=landscape_original, tiempo=tiempo+1, ruta=ruta_generacion)            

                self.recorrer_secuencias(data=landscape_filtrado, ruta=ruta_generacion, tiempo=tiempo+1)

    def generar_landscape_original(self, secuencia, tiempo, ruta):
        data = self.run(secuencia)
        data["respuesta"] = np.random.normal(0,1,len(data))
        ruta_exportar = os.path.join(ruta, f"landscape_original_G{tiempo}.csv")
        data.to_csv(ruta_exportar, index=False, header=True)

        return data
    
    def filtrar_landscape(self, data, tiempo, ruta):
        umbral = data["respuesta"].quantile(self.p)
        data = data[data["respuesta"] >= umbral]
        ruta_exportar = os.path.join(ruta, f"landscape_filtrado_G{tiempo}.csv")
        data.to_csv(ruta_exportar, index=False, header=True)

        return data

    def crear_directorio_generacion(self, ruta, tiempo):
        ruta_generacion = os.path.join(ruta, f"G{tiempo}")
        os.mkdir(ruta_generacion)

        return ruta_generacion

    def recorrer_secuencias(self, data, ruta, tiempo):
        for i in range(len(data)):
            mutation = data["wild"].iloc[i] + data["position"].iloc[i].astype(str) + data["mutant"].iloc[i]
            ruta_carpeta_seq = os.path.join(ruta, mutation)
            os.mkdir(ruta_carpeta_seq)
            self.generaciones(secuencia=data["seq"].iloc[i], tiempo=tiempo, ruta=ruta_carpeta_seq)
    
    def generar_data_grafo(self, ruta, tiempo, nodo_unir=''):
        primer_directorio = os.path.join(ruta, f"G{tiempo}")
        for dir in os.listdir(primer_directorio):
            if os.path.splitext(dir)[1] != ".csv":
                nombre_nodo1 = f"G{tiempo}-{dir}"
                self.dot.node(nombre_nodo1, nombre_nodo1)

                if nodo_unir != '':
                    self.edges.append([nodo_unir, nombre_nodo1])

                if tiempo + 1 <= self.g:
                    nueva_ruta = os.path.join(primer_directorio, dir)
                    self.generar_data_grafo(ruta=nueva_ruta, tiempo=tiempo+1, nodo_unir=nombre_nodo1)

                if tiempo == 1:
                    self.dot.edges(self.edges)
                    ruta_exportar = os.path.join(ruta, f"G{tiempo}", dir, f"G{tiempo} - {dir}")
                    self.dot.filename = ruta_exportar
                    self.dot.format = "png"
                    self.dot.render()    
                    self.dot = graphviz.Digraph()
                    self.edges = []
                
            
            