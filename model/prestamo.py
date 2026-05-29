from model.libro import Libro
from model.persona import Persona
from model.persona import Estudiante
from datetime import datetime, timedelta

class Prestamo:
    def __init__(self, libro: Libro, estudiante: Estudiante, fecha_inicio = datetime.now(), fecha_devolucion = (datetime.now()+timedelta(0,0,0,0,2,0,0)),estado_prestamo = "Prestado")->None:
        self.libro = libro
        self.estudiante = estudiante
        self.fecha_inicio = fecha_inicio
        self.fecha_devolucion = fecha_devolucion
        self.estado_prestamo = estado_prestamo
    def __str__(self)->str:
        return f"Libro prestado: '{self.libro.titulo}'\nEstudiante: {self.estudiante.codigo}\nFecha de inicio: {self.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\nFecha de devolucion: {self.fecha_devolucion.strftime("%d/%m/%Y %H:%M")}\nEstado: {self.estado_prestamo}"
    def actualizar_estado(self,estado_prestamo="")->None:
        if( self.fecha_devolucion <= datetime.today() and self.estado_prestamo != "Devuelto"):
            self.estado_prestamo = "Vencido"
        if(estado_prestamo=="Devuelto"):
            self.estado_prestamo = "Devuelto"