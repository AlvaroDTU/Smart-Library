from model.libro import Libro
from model.persona import Bibliotecario
from model.persona import Estudiante
from model.prestamo import  Prestamo

from repository.estudiante_repository import EstudianteRepository
from repository.bibliotecario_repository import BibliotecarioRepository
from repository.prestamo_repository import PrestamoRepository
from repository.libro_repository import LibroRepository

from service.bibliotecario_service import BibliotecarioService
from service.estudiante_service import EstudianteService
from service.prestamo_service import PrestamoService
from service.libro_service import LibroService

class ReporteService:
    
    def __init__(self, estudiante_repo:EstudianteRepository, biliotecario_repo:BibliotecarioRepository, libro_repo:LibroRepository, prestamo_repo:PrestamoRepository):
        self.estudiante_repo = estudiante_repo
        self.bibliotecario_repo = biliotecario_repo
        self.libro_repo = libro_repo
        self.prestamo_repo = prestamo_repo
        

    def reporte_estudiante(self)->list[dict]:
        return [
                {
                    "Nombre": estudiante.nombre,
                    "Codigo": estudiante.codigo,
                    "Carrera": estudiante.carrera,
                    "Email": estudiante.email,
                    "Cantidad de prestamos": estudiante.cantidad_prestamos,
                }
                for estudiante in self.estudiante_repo.listar()
                ]

    def reporte_bibliotecarios(self)->list[dict]:
        return [
                {
                    "Nombre": bibliotecario.nombre,
                    "Codigo": bibliotecario.codigo,
                    "Tipo de acceso": bibliotecario.nivel_acceso,
                    "Email": bibliotecario.email,
                }
                for bibliotecario in self.bibliotecario_repo.listar()
                ]

    def reporte_vencidos(self)->list[dict]:
        
        return [
                {
                    "Codigo estudiante": prestamos.estudiante.codigo,
                    "Titulo": prestamos.libro.titulo,
                    "Estado": prestamos.estado_prestamo,
                }
                for prestamos in self.prestamo_repo.listar() if prestamos.estado_prestamo == "Vencido"
                ]

    def recomendaciones_Libros(self)->str | None:
        libros = self.libro_repo.listar()
        libros_ordenados = sorted(libros, key=lambda libro: libro._cantidad_prestamos, reverse=True)
        return libros_ordenados[0]

