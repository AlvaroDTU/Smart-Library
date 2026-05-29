import os
from helper.csv_helper import CsvHelper
from datetime import datetime,timedelta
from model.prestamo import Prestamo
from model.libro import Libro
from model.persona import Estudiante

from repository.estudiante_repository import EstudianteRepository
from repository.libro_repository import LibroRepository

class PrestamoRepository:
    def __init__(self, estudiante_repo: EstudianteRepository, libro_repo: LibroRepository, ruta : str = 'data/prestamos.csv')->None:
        self._estudiante_repo = estudiante_repo
        self._libro_repo = libro_repo
        self.prestamos : list = []
        self._ruta = ruta
        self._cargar()

    def guardar(self,prestamo: Prestamo)->None:
        self.prestamos.append(prestamo)
        self._persisitir()

    def buscar_por_libro(self, isbn: str)-> list[Prestamo] | None:
        libro = self._libro_repo.buscar_por_isbn(isbn)
        if libro is None:
            print(f"Libro con isbn '{isbn}' no ha sido encontrado")
            return
        return [prestamo for prestamo in self.prestamos if prestamo.libro.isbn == isbn]

    def buscar_por_estudiante(self, codigo: str)->list[Prestamo] | None:
        estudiante = self._estudiante_repo.buscar_por_codigo(codigo)
        if estudiante is None:
            print(f"Estudiante con codigo '{codigo}' no ha sido encontrado")
            return
        return [prestamo for prestamo in self.prestamos if prestamo.estudiante.codigo == codigo]

    def actualizar_estado(self, codigo : str, isbn : str, estado:str) -> None:
        for prestamo in self.prestamos:
            if(prestamo.estudiante.codigo == codigo and prestamo.libro.isbn == isbn):
                prestamo.actualizar_estado(estado)
        self._persisitir()

    def actualizar_estado_general(self) -> None:
        for prestamo in self.prestamos:
            prestamo.actualizar_estado()
        self._persisitir()

    def listar(self)-> list[Prestamo]:
        return list(self.prestamos)

    def _cargar(self):
        
        for fila in CsvHelper.cargar(self._ruta):
            libro = self._libro_repo.buscar_por_isbn(fila["ISBN del libro"])
            estudiante = self._estudiante_repo.buscar_por_codigo(fila["Codigo del estudiante"])
            fecha_inicio = datetime.strptime(fila["Fecha de inicio"],"%d/%m/%Y %H:%M")
            fecha_devolucion = datetime.strptime(fila["Fecha de devolucion"],"%d/%m/%Y %H:%M")
            prestamo = Prestamo(libro,estudiante,fecha_inicio,fecha_devolucion,fila["Estado de prestamo"])
            self.prestamos.append(prestamo)

    def _persisitir(self):
        encabezados = ["Codigo del estudiante", "Titulo del libro","ISBN del libro", "Fecha de inicio", "Fecha de devolucion","Estado de prestamo"]
        filas = [
            [p.estudiante.codigo,p.libro.titulo,p.libro.isbn,p.fecha_inicio.strftime("%d/%m/%Y %H:%M"),p.fecha_devolucion.strftime("%d/%m/%Y %H:%M"),p.estado_prestamo]
            for p in self.prestamos
        ]
        CsvHelper.guardar(self._ruta,encabezados,filas)