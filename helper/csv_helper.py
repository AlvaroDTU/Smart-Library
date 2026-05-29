import csv
import os

class CsvHelper:
    @staticmethod
    def guardar(ruta: str, encabezados: list[str], filas: list[list]) -> None:
        carpeta = os.path.dirname(ruta)
        if carpeta:
            os.makedirs(carpeta, exist_ok=True)
            with open(ruta, "w", newline="", encoding="utf-8") as archivo:
                writer = csv.writer(archivo)
                writer.writerow(encabezados)
                writer.writerows(filas)

    @staticmethod
    def cargar(ruta: str) -> list[dict]:
        if not os.path.exists(ruta):
            raise ValueError(f"El archivo {ruta} no existe.")
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            reader = csv.DictReader(archivo)
            return [fila for fila in reader]
