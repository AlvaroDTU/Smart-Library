from model.persona import Autor

class Libro:
    def __init__(self, isbn:str, titulo:str, autor: Autor, categoria:str, stock: int, cantidad_prestamos: int = 0):
        self.isbn = isbn 
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.stock = stock
        self._cantidad_prestamos = cantidad_prestamos

    def __str__(self):
        return f"ISBN: {self.isbn}\n'{self.titulo}' de {self.autor.nombre} - {self.categoria}\nStock: {self.stock}\n"
    
    def disponible(self):
        return self.stock > 0
    
    def actualizar_stock(self, cantidad: int):
        self.stock += cantidad

    def aumentar_prestamos(self):
        self._cantidad_prestamos += 1
    
