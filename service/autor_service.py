from helper.csv_helper import CsvHelper

from model.persona import Autor
from repository.autor_repository import AutorRepository

class AutorService:
    def __init__(self, autor_repo : AutorRepository):
        self.repo = autor_repo
    
    def registrar_autor(self,codigo:str, nombre:str, email:str)-> Autor | None:
        if self.repo.buscar_por_codigo(codigo) is not None:
            print(f"Autor de codigo '{codigo}'a registrado")
            return
        autor = Autor(nombre,codigo,email)
        self.repo.guardar(autor)
        return autor
    
    def buscar_por_codigo(self,codigo:str) -> Autor | None:
        autor = self.repo.buscar_por_codigo(codigo)
        if autor is None:
            print(f"Autor de codigo '{codigo}' no existe")
            return
        return autor
    
    def listar(self) -> list:
        return self.repo.listar()