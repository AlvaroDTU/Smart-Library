from model.persona import Bibliotecario
from repository.bibliotecario_repository import BibliotecarioRepository

class BibliotecarioService:
    def __init__(self, bibliotecario_repo: BibliotecarioRepository):
        self._repo : BibliotecarioRepository = bibliotecario_repo

    def registrar_bibliotecario(self, nombre: str, codigo: str, email: str, nivel_acceso: int)->Bibliotecario | None:
        if self._repo.buscar_por_codigo(codigo) is not None:
            print(f"Bibliotecario de codigo '{codigo}' ya existente en el sistema")
            return
        bibliotecario = Bibliotecario(nombre,codigo,email,nivel_acceso)
        self._repo.guardar(bibliotecario)   
        return bibliotecario

    def buscar_bibliotecario(self,codigo) -> Bibliotecario:
        bibliotecario = self._repo.buscar_por_codigo(codigo)
        if bibliotecario is not None:
            return bibliotecario
        else:
            print(f"Bibliotecario de codigo {codigo} no existe")

    def listar_bibliotecarios(self) -> list[Bibliotecario]:
        return self._repo.listar()

    def eliminar_bibliotecario(self,codigo):
        self._repo.eliminar_bibliotecario(codigo)
        if codigo in self._repo.bibliotecarios:
            self._repo.eliminar_bibliotecario(codigo)