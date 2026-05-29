from model.persona import Estudiante
from repository.estudiante_repository import EstudianteRepository

class EstudianteService:
    def __init__(self, estudiante_repo : EstudianteRepository):
        self._repo : EstudianteRepository = estudiante_repo

    def registrar_estudiante(self, nombre: str, codigo: str, email: str, carrera: str)->Estudiante:
        if self._repo.buscar_por_codigo(codigo) is not None:
            print(f"Estudiante de codigo '{codigo}' ya existente")
            return
        estudiante = Estudiante(nombre,codigo,email,carrera)
        self._repo.guardar(estudiante) 
        return estudiante

    def buscar_estudiante(self, codigo) -> Estudiante | None:
        estudiante =  self._repo.buscar_por_codigo(codigo)
        if estudiante is None:
            print(f"Estudiante de codigo '{codigo}' no existe")
        return estudiante

    def listar_estudiantes(self) -> list[Estudiante]:
        return self._repo.listar()

    def eliminar_estudiante(self, codigo):
        estudiante = self.buscar_estudiante(codigo)
        if estudiante is not None:
            self._repo.eliminar_estudiante(codigo)