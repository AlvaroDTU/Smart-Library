import os
from model.persona import Estudiante
from helper.csv_helper import CsvHelper

class EstudianteRepository:
    def __init__(self, ruta: str = 'data/estudiantes.csv')->None:
        self.estudiantes: dict = {} # codigo -> estudiante o bibliotecario
        self._ruta = ruta
        self._cargar()

    def guardar(self, estudiante: Estudiante)-> None:
        self.estudiantes[estudiante.codigo] = estudiante
        self._persistir()

    def buscar_por_codigo(self,codigo: str)-> Estudiante | None:
        return self.estudiantes.get(codigo)

    def listar(self)-> list[Estudiante]:
        return list(self.estudiantes.values())

    def eliminar_estudiante(self, codigo: str)->None:
        del self.estudiantes[codigo]
        self._persistir()

    def aumentar_prestamos(self,codigo : str)->None:
        self.estudiantes.get(codigo).aumentar_prestamos()
        self._persistir()

    def _cargar(self)->None:
        for fila in CsvHelper.cargar(self._ruta):
            estudiante = Estudiante(fila["Nombre"],fila["Codigo"],fila["Email"],fila["Carrera"],int(fila["Prestamos pedidos"]))
            self.estudiantes[estudiante.codigo] = estudiante

    def _persistir(self) -> None:
        encabezados = ["Codigo","Nombre","Email","Carrera","Prestamos pedidos"]
        filas = [
            [e.codigo,e.nombre,e.email,e.carrera,e.cantidad_prestamos]
            for e in self.estudiantes.values()
        ]
        CsvHelper.guardar(self._ruta,encabezados,filas)