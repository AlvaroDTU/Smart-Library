from model.prestamo import Prestamo
from model.libro import Libro
from model.persona import Estudiante
from repository.libro_repository import LibroRepository
from repository.estudiante_repository import EstudianteRepository
from repository.prestamo_repository import PrestamoRepository

class PrestamoService:
    def __init__(self, prestamo_repo : PrestamoRepository, libro_repo: LibroRepository, estudiante_repo: EstudianteRepository) -> None:
        self._prestamo_repo = prestamo_repo
        self._libro_repo = libro_repo
        self._estudiante_repo = estudiante_repo

    def registrar_prestamo(self, isbn: str, codigo: str) -> None:
        self._prestamo_repo.actualizar_estado_general()
        libro = self._libro_repo.buscar_por_isbn(isbn)
        estudiante = self._estudiante_repo.buscar_por_codigo(codigo)
        if libro is None:
            print(f"No existe el libro con isbn '{isbn}'")
            return
        if estudiante is None:
            print(f"No existe estudiante con codigo '{codigo}'")
            return
        if not libro.disponible():
            print(f"El libro '{libro.titulo}' no tiene stock disponible, vuelva mas tarde.")
            return
        prestamo = Prestamo(libro,estudiante)
        self._prestamo_repo.guardar(prestamo)
        self._estudiante_repo.aumentar_prestamos(codigo)
        self._libro_repo.actualizar_stock(isbn,-1)
        self._libro_repo.aumentar_prestamos(isbn)
        print(f"Prestamo del libro '{libro.titulo}' realizado con exito!")

    def buscar_por_libro(self, isbn: str) -> list[Prestamo]:
        self._prestamo_repo.actualizar_estado_general()
        libro = self._libro_repo.buscar_por_isbn(isbn)
        if libro is None:
            print(f"No existe el libro con isbn '{isbn}'")
        return self._prestamo_repo.buscar_por_libro(isbn)
    
    def buscar_por_estudiante(self, codigo: str) -> list[Prestamo] | None:
        self._prestamo_repo.actualizar_estado_general()
        estudiante = self._estudiante_repo.buscar_por_codigo(codigo)
        if estudiante is None:
            print(f"No existe estudiante con codigo '{codigo}'")
            return
        return self._prestamo_repo.buscar_por_estudiante(codigo)
    
    def devolver_prestamo(self,isbn:str,codigo:str) -> None:
        self._prestamo_repo.actualizar_estado_general()
        estudiante =self._estudiante_repo.buscar_por_codigo(codigo)
        libro = self._libro_repo.buscar_por_isbn(isbn)
        if estudiante is None:
            print(f"No existe el estudiante '{codigo}' en nuestro sistema")
            return
        if libro is None:
            print(f"No existe el libro '{isbn}' en nuestro sistema")
            return
        contador = 0
        for prestamo in self._prestamo_repo.listar():
            if prestamo.estudiante.codigo == codigo and prestamo.libro.isbn == isbn and (prestamo.estado_prestamo == "Prestado" or prestamo.estado_prestamo == "Vencido"):
                self._libro_repo.actualizar_stock(isbn,1)
                self._prestamo_repo.actualizar_estado(codigo,isbn,"Devuelto")
                contador+=1
                break
        if contador<=0:
            print(f"Estudiante '{codigo}' no ha pedido prestado el libro con isbn'{isbn}'")
            return
        print(f"Libro '{libro.titulo}' devuelto con exito por el estudiante {estudiante.nombre}")

    def listar_prestamos(self)->list[Prestamo]:
        return self._prestamo_repo.listar()

