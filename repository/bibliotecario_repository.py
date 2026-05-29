import os

from model.persona import Bibliotecario
from helper.csv_helper import CsvHelper

class BibliotecarioRepository:
    def __init__(self, ruta:str = 'data/bibliotecarios.csv')->None:
        self._ruta = ruta
        self.bibliotecarios = {} # estructura: dic (codigo -> bibliotecario)
        self._cargar()

    def guardar(self, bibliotecario: Bibliotecario)->None:
        self.bibliotecarios[bibliotecario.codigo] = bibliotecario
        self._persistir()

    def _cargar(self) ->None:
        for fila in CsvHelper.cargar(self._ruta):
            bibliotecario = Bibliotecario(fila["Nombre"],fila["Codigo"],fila["Email"],int(fila["Nivel de Acceso"]))
            self.bibliotecarios[bibliotecario.codigo] = bibliotecario

    def buscar_por_codigo(self, codigo) -> Bibliotecario |  None:
        return self.bibliotecarios.get(codigo)

    def listar(self)->list[Bibliotecario]:
        return list(self.bibliotecarios.values())

    def eliminar_bibliotecario(self, codigo)->None:
        del self.bibliotecarios[codigo]
        self._persistir()

    def _persistir(self)->None:
        encabezados = ["Codigo", "Nombre", "Email", "Nivel de Acceso"]
        
        filas = [
            [b.codigo,b.nombre,b.email,b.nivel_acceso]
            for b in self.bibliotecarios.values()
        ]
        
        CsvHelper.guardar(self._ruta, encabezados, filas)