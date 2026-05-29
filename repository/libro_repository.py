import os
from model.libro import Libro 
from helper.csv_helper import CsvHelper

class LibroRepository:
    def __init__(self, ruta : str = 'data/libros.csv'):
        self.libros = {}
        self._ruta = ruta
        self._cargar()

    def agregar_libro(self, libro):
        self.libros[libro.isbn] = libro
        self._persistir()

    def buscar_por_isbn(self, isbn) -> Libro | None:
        return self.libros.get(isbn)

    def eliminar_libro(self, isbn)->None:
        del self.libros[isbn]
        self._persistir()

    def actualizar_stock(self, isbn : str,stock: int):
        self.libros.get(isbn).actualizar_stock(stock)
        self._persistir()

    def aumentar_prestamos(self,isbn : str):
        self.libros.get(isbn).aumentar_prestamos()
        self._persistir()

    def listar(self)-> list[Libro]:
        return list(self.libros.values())

    def _cargar(self)->None:
        for fila in CsvHelper.cargar(self._ruta):
            libro = Libro(fila["ISBN"],fila["Titulo"],fila["Autor"],fila["Categoria"], int(fila["Stock"]),int(fila["Cantidad prestamos"]))
            self.libros[libro.isbn] = libro
            
    def _persistir(self)->None:
        encabezados = ["ISBN","Titulo","Autor","Categoria","Stock","Cantidad prestamos"]
        filas = [
            [l.isbn,l.titulo,l.autor,l.categoria,l.stock,l._cantidad_prestamos]
            for l in self.libros.values()
        ]
        CsvHelper.guardar(self._ruta,encabezados,filas)