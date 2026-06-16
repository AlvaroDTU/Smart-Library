from model.libro import Libro
from model.persona import Autor
from repository.autor_repository import AutorRepository
from repository.libro_repository import LibroRepository

class LibroService:
    def __init__(self, libro_repo : LibroRepository, autor_repo:AutorRepository)->None:
        self._repo: LibroRepository = libro_repo
        self._autor_repo: AutorRepository = autor_repo

    def registrar_libro(self, isbn : str,titulo : str, codigo_autor:str, categoria : str, stock : int)->Libro | None:
        if self._repo.buscar_por_isbn(isbn) is not None:
            print(f"Libro de isbn '{isbn}' ya registrado")
            return
        autor = self._autor_repo.buscar_por_codigo(codigo_autor)
        if autor is None:
            print(f"No se encontre al autor de codigo '{codigo_autor}', pruebe registrando a un nuevo autor")
            return
        libro = Libro(isbn,titulo,autor,categoria,stock)
        self._repo.agregar_libro(libro) 
        print(f"Nuevo Libro registrado: {libro.titulo}")
        return libro

    def buscar_libro(self,isbn : str)-> Libro | None:
        libro = self._repo.buscar_por_isbn(isbn)
        if libro is None:
            print(f"Libro con ISBN {isbn} no existe")
        return libro
    
    def buscar_libro_titulo(self,titulo : str)-> list[Libro] | None:
        libros_encontrados = [libro for libro in self._repo.listar() if libro.titulo == titulo]
        if not libros_encontrados:
            print(f"Libro de titulo {titulo} no encontrado")
            return
        return libros_encontrados
    
    def buscar_libro_categoria(self,categoria : str)->list[Libro] | None:
        categorias_encontradas = [libro for libro in self._repo.listar() if libro.categoria == categoria]
        if not categorias_encontradas:
            print(f"Categoria {categoria} no encontrada")
            return
        return  categorias_encontradas
    
    def listar_libros(self)->list[Libro]:
        return self._repo.listar()

    def actualizar_stock(self, isbn,stock: int) -> None:
        libro = self._repo.buscar_por_isbn(isbn)
        if(libro is None):
            print(f"Libro con isbn '{isbn}' no encontrado")
            return
        if(stock<0 and libro.stock+stock<0): 
                print(f"No puedes reducir el stock a menos de 0")
                return
        
        if stock>0:
            print(f"Se agrego {stock} libros a {libro.titulo}")
        else:
            print(f"Se quito {-stock} libros a {libro.titulo}")
        self._repo.actualizar_stock(isbn, stock)

    def eliminar_libro(self, isbn) -> None:
        libro = self.buscar_libro(isbn)
        if libro is not None:
            self._repo.eliminar_libro(isbn)