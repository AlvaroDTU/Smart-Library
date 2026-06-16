from model.persona import Autor
from helper.csv_helper import CsvHelper
class AutorRepository:
    def __init__(self, ruta ='data/autores.csv')->None:
        self.autores : dict = {}
        self._ruta = ruta
        self._cargar()
        
    def guardar(self, autor : Autor)->None:
        self.autores[autor.codigo] = autor
        self.guardar()
    
    def buscar_por_codigo(self, codigo: str)-> Autor | None:
        return self.autores.get(codigo)

    def listar(self):
        return list(self.autores.values())
    
    def _persistir(self):
        encabezados = ['Código','Nombre']
        filas = [ 
            [a.codigo, a.nombre] 
            for a in self.autores.values()
        ]
        
        CsvHelper.guardar(self._ruta,encabezados,filas)
        
    def _cargar(self):
        for fila in CsvHelper.cargar(self._ruta):
            autor = Autor(fila['Nombre'],fila['Codigo'])
            self.autores[autor.codigo] = autor