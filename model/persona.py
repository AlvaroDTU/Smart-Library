class Persona:
    def __init__(self, nombre: str, codigo: str, email: str) -> None:
        self.nombre = nombre
        self.codigo = codigo
        self.email = email

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}, {self.email}"

class Estudiante(Persona):
    def __init__(self, nombre: str, codigo: str, email: str, carrera: str, cantidad_prestamos: int = 0) -> None:
        super().__init__(nombre, codigo.upper(), email)
        self.carrera = carrera
        self.cantidad_prestamos= cantidad_prestamos
    
    def __str__(self) -> str:
        return  f"[ESTUDIANTE] {super().__str__()} , Carrera: {self.carrera}"
    
    def aumentar_prestamos(self) -> None:
        self.cantidad_prestamos += 1

class Bibliotecario(Persona):
    def __init__(self, nombre: str, codigo: str, email: str, nivel_acceso: int) -> None:
        super().__init__(nombre, codigo.upper(), email)
        self.nivel_acceso = nivel_acceso
        
    def __str__(self) -> str:
        if(self.nivel_acceso==1):
            return f"[BIBLIOTECARIO] {super().__str__()} | Nivel de acceso: {self.nivel_acceso}"
        return f"[ADMINISTRADOR] {super().__str__()} | Nivel de acceso: {self.nivel_acceso}"
    
class Autor(Persona):
    def __init__(self, nombre: str, codigo: str) -> None:
        self.nombre = nombre
        self.codigo = codigo
    
    def __str__(self) -> str:
        return f"[AUTOR] {self.codigo} - {self.nombre}"