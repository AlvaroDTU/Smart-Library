from model.libro import Libro
from model.persona import Bibliotecario
from model.persona import Estudiante
from model.persona import Autor
from model.prestamo import  Prestamo

from repository.estudiante_repository import EstudianteRepository
from repository.bibliotecario_repository import BibliotecarioRepository
from repository.prestamo_repository import PrestamoRepository
from repository.libro_repository import LibroRepository
from repository.autor_repository import AutorRepository

from service.bibliotecario_service import BibliotecarioService
from service.estudiante_service import EstudianteService
from service.prestamo_service import PrestamoService
from service.libro_service import LibroService
from service.reporte_service import ReporteService
from service.autor_service import AutorService

def cargar_datos_iniciales(estudiantes_service,bibliotecarios_service,libros_service):
    bibliotecarios_service.registrar_bibliotecario("Alvaro De Tomas","B20251N440","alvarosteven69@gmail.com",2)
    bibliotecarios_service.registrar_bibliotecario("Jefferson Cobeñas","B20251J487","CodigSub14@gmail.com",2)
    bibliotecarios_service.registrar_bibliotecario("Alexandra Armas","B20251J464","Macitlv_plks@gmail.com",2)

    libros_service.registrar_libro("ISBN-001","Cien anos de soledad","Gabriel Garcia Marquez","Novela",0)
    libros_service.registrar_libro("ISBN-002","Don Quijote de la Mancha","Miguel de Cervantes","Clasico",3)
    libros_service.registrar_libro("ISBN-003","La ciudad y los perros","Mario Vargas Llosa","Novela",4)
    libros_service.registrar_libro("ISBN-004","Tradiciones peruanas","Ricardo Palma","Literatura peruana",6)
    libros_service.registrar_libro("ISBN-005","Los ríos profundos","Jose Maria Arguedas","Literatura peruana",2)

    estudiantes_service.registrar_estudiante("Lucía Fernández", "U20251L205", "lucia.fernandez@upc.edu.pe", "Ingeniería de Software")
    estudiantes_service.registrar_estudiante("Diego Ramírez", "U20251D731", "diego.ramirez@upc.edu.pe", "Ingeniería de Sistemas")
    estudiantes_service.registrar_estudiante("Andrea Torres", "U20251C458", "andrea.torres@upc.edu.pe", "Ingenieria Civil")
    estudiantes_service.registrar_estudiante("Sebastián Vargas", "U20251S926", "sebastian.vargas@upc.edu.pe", "Ingeniería de Software")
    estudiantes_service.registrar_estudiante("Valeria Mendoza", "U20251V347", "valeria.mendoza@upc.edu.pe", "Ciencias de la Computación")
    estudiantes_service.registrar_estudiante("Mateo Castillo", "U20251M583", "mateo.castillo@upc.edu.pe", "Ingeniería de Sistemas")
    estudiantes_service.registrar_estudiante("Daniela Rojas", "U20251D814", "daniela.rojas@upc.edu.pe", "Ciencia de Datos")

def mostrar_menu(tipo_acceso: int):
    print()
    print("=== SmartLibrary - Prestamos y consultas de libros ===")
    print()
    print("1. Consultar mis datos")
    print("2. Realizar prestamo")
    print("3. Realizar devolucion")
    print("4. Consultar libros") # dentro va a ser por isbn, por titulo o por categoria
    print("5. Mi historial de prestamos")
    print()
    print("--- Reportes ---")
    print("6. Recomendaciones de libros")
    print("7. Reporte de prestamos vencidos")
    print("8. Reporte de estudiantes")
    print("9. Reporte de bibliotecarios")
    print()
    if(tipo_acceso >= 1):  
        print("--- Bibliotecarios ---")
        print("10. Registrar estudiante")
        print("11. Eliminar estudiante") 
        print("12. Listar historial de prestamos")
        print("13. Añadir o quitar stock a un libro")
        print("14. Añadir o quitar libros")
        print()
    if(tipo_acceso >= 2):
        print("--- Administradores ---")
        print("15. Registrar bibliotecario")
        print("16. Eliminar bibliotecario")
    print("0. Salir")
    print()

def validar_codigo_estudiante():
    while (True):
        codigo = input("Ingrese su codigo de alumno : ").upper()
        if codigo[0] != "U":
            print("Debe inciar con U")
            continue
        if len(codigo) != 10:
            print("Codigo no valido, debe tener 10 caracteres")
            continue
        break
    return codigo

def main():
    estudiantes_repo = EstudianteRepository()
    bibliotecarios_repo = BibliotecarioRepository()
    autores_repo = AutorRepository()
    libros_repo = LibroRepository(autores_repo)
    prestamos_repo = PrestamoRepository(estudiantes_repo,libros_repo)

    estudiantes_service = EstudianteService(estudiantes_repo)
    bibliotecarios_service = BibliotecarioService(bibliotecarios_repo)
    autores_service = AutorService(autores_repo)
    libros_service = LibroService(libros_repo, autores_repo)
    prestamos_service = PrestamoService(prestamos_repo, libros_repo, estudiantes_repo)

    reporte_service = ReporteService(estudiantes_repo,bibliotecarios_repo,libros_repo,prestamos_repo) 
    if not libros_repo.listar() and not estudiantes_repo.listar() and not bibliotecarios_repo.listar():
        cargar_datos_iniciales(estudiantes_service,bibliotecarios_service,libros_service)
        print("Datos iniciales cargados desde la funcion")
    else:
        print(f"Datos cargados desde CSV: {len(estudiantes_repo.listar())} estudiantes, {len(libros_repo.listar())} libros ,{len(bibliotecarios_repo.listar())} bibliotecarios y {len(autores_repo.listar())} autores")

    codigo_1 = "B20251N440"
    codigo_2 = "B20251J487"
    codigo_3 = "B20251J897"
    estado = []
    tipo_acceso = 0
    while(True):
        codigo_acceder = input("Ingrese su codigo (0 para salir): ").upper()
        if codigo_acceder == "0":
            break
        if codigo_acceder[0] != 'B' and codigo_acceder[0] != 'U':
            print("Codigo no valido, debe empezar con 'B' para bibliotecarios o 'U' para estudiantes")
            continue
        if len(codigo_acceder)!= 10:
            print("Codigo no valido, debe tener 10 caracteres")
            continue
        if codigo_acceder[0] == 'B':
            usuario = bibliotecarios_repo.buscar_por_codigo(codigo_acceder)
            if usuario is None:
                print("Acceso prohibido, bibliotecario no encontrado en nuestra base de datos")
                continue
            if usuario.codigo == codigo_1 or usuario.codigo == codigo_2 or usuario.codigo == codigo_3:
                print("Acceso de administrador\n")
                tipo_acceso = 2
                break
            print("Acceso de bibliotecario\n")
            tipo_acceso = 1
            break
        if codigo_acceder[0] == 'U':
            usuario = estudiantes_repo.buscar_por_codigo(codigo_acceder)
            if usuario is None:
                print("No te encuentras registrado en nuestra base de datos, contacta a un bibliotecario para que te registre")
                continue
            print("Acceso de estudiante\n")
            tipo_acceso = 0
            estado = [prestamo 
                for prestamo in prestamos_repo.buscar_por_estudiante(usuario.codigo)
                if prestamo.estado_prestamo == "Vencido" or prestamo.estado_prestamo == "Prestado"]
            break
        
    if codigo_acceder == "0":
        print("Saliendo del sistema...")
        return
    print(f"Bienvenido, {usuario.nombre}!")
    if estado:
        print("\n--- Tienes libros pendientes ---")
        for prestamo in estado:
            print(f"{prestamo.libro.titulo} | Estado: {prestamo.estado_prestamo}")

    while(True):
        mostrar_menu(tipo_acceso)
        opcion = input("Elija una opcion: ")
        if opcion == "1":
            while (True):
                codigo = input("Ingrese su codigo de alumno : ").upper()
                if codigo[0] != "U":
                    print("Debe inciar con U")
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            estudiante = estudiantes_service.buscar_estudiante(codigo)
            print(estudiante)
        
        elif opcion == "2":
            while (True):
                codigo = input("Ingrese su codigo de estudiante: ").upper()
                if codigo[0] != "U":
                    print("Debe inciar con U")
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            while(True):
                isbn = input("Ingrese isbn del libro que va a pedir: ").upper()
                if isbn[:5] != "ISBN-":
                    print("Debes iniciar con ISBN-")
                    continue
                break   
            prestamo = prestamos_service.registrar_prestamo(isbn,codigo)
        
        elif opcion == "3":
            while (True):
                codigo = input("Ingrese su codigo de estudiante: ").upper()
                if codigo[0] != "U":
                    print("Debe inciar con U")
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            while(True):
                isbn = input("Ingrese isbn del libro a devolver: ").upper()
                if isbn[:5] != "ISBN-":
                    print("Debes iniciar con ISBN-")
                    continue
                break   
            prestamos_service.devolver_prestamo(isbn,codigo)
        elif opcion == "4":
            op = input("Que tipo de busqueda desea? (1: General, 2: por ISBN, 3: por titulo, 4: por categoria): ")
            if(op == "1"):
                print("-----Libros de SmartLibrary-----")
                print(*libros_service.listar_libros(),sep="\n")
            elif(op == "2"):
                while(True):
                    isbn = input("Ingrese el isbn de busqueda (ISBN-xxx): ").upper()
                    if isbn[:5] != "ISBN-":
                        print("Debes iniciar con ISBN-")
                        continue
                    break   
                    
                libro = libros_service.buscar_libro(isbn)
                if libro is not None:
                    print("Libro encontrado!")
                    print(libro)
            elif(op == "3"):
                titulo = input("Ingrese el titulo a buscar: ")
                libros_encontrados = libros_service.buscar_libro_titulo(titulo)
                if libros_encontrados:
                    print(*libros_encontrados,sep="\n")
        
            elif(op == "4"):
                categoria = input("Ingrese la categoria a buscar: ")
                libros_encontrados = libros_service.buscar_libro_categoria(categoria)
                if libros_encontrados:
                    print(*libros_encontrados,sep="\n")
            else:
                print("Opcion de busqueda invalida")
        
        elif (opcion == "5"):
            while (True):
                codigo = input("Ingrese su codigo de estudiante: ").upper()
                if codigo[0] != "U":
                    print("Debe inciar con U")
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            if not prestamos_service.buscar_por_estudiante(codigo):
                continue
            print("---Prestamos realizados---")
            for prestamo in prestamos_service.buscar_por_estudiante(codigo):
                print(f"{prestamo}\n")
        
        elif (opcion == "6"):
            print("Te recomendamos este libro que fue el mas prestado de la semana: ")
            print(reporte_service.recomendaciones_Libros(),sep="\n")
        
        elif (opcion == "7"):
            print("-----Prestamos Vencidos-----")
            print(reporte_service.reporte_vencidos(),sep="\n")
                
        elif (opcion == "8"):
            print(*reporte_service.reporte_estudiante(),sep="\n")
        
        elif (opcion =="9"):
            print(*reporte_service.reporte_bibliotecarios(),sep="\n")    
        
        elif (opcion == "10"):
            nombre = input("Ingrese nombre del estudiante (Apellidos, Nombres): ")
            while (True):
                codigo = input("Ingrese el codigo de estudiante: ").upper()
                if codigo[0] != "U":
                    print("Debe inciar con U")
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            email = input("Ingrese el correo electronico: ")
            carrera = input("Ingrese la carrera: ")
            estudiante = estudiantes_service.registrar_estudiante(nombre,codigo,email,carrera)
            print(f"Registrado: {estudiante.nombre}")
        
        elif (opcion == "11"):
            while (True):
                codigo= input("Ingrese el codigo del estudiante a eliminar: ").upper()
                if codigo[0] != "U":
                    print("Codigo no valido, debe empezar con U") 
                    continue
                if len(codigo) != 10:
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            estudiantes_service.eliminar_estudiante(codigo)

        elif (opcion == "12"):
            if prestamos_service.listar_prestamos():
                print("-----Prestamos------")
                print(*prestamos_service.listar_prestamos(),sep="\n")
            else:
                print("No hay prestamos en el sistema")

        elif (opcion == "13"):
            op = int(input("Agregar Stock(1) | Eliminar Stock(2) : " ))
            if(op==1): 
                while (True):
                    isbn = input("Escriba el isbn del libro: ").upper()
                    if isbn[:5] != "ISBN-":
                        print("Debes iniciar con 'ISBN-'")
                        continue
                    break
                while(True):
                    cantidad = int(input("Escriba la cantidad de stock a agregar: "))
                    if cantidad < 0:
                        print("Cantidad no valida, debe ser un numero positivo")
                        continue
                    break
                libros_service.actualizar_stock(isbn,cantidad)
                

            elif (op == 2):
                while (True):
                    isbn = input("Ingrese el isbn del libro: ").upper()
                    if isbn[:5] != "ISBN-":
                        print("Debes iniciar con 'ISBN-' ")
                        continue
                    break
                while(True):
                    cantidad = int(input("Escriba la cantidad de stock a quitar: "))
                    if cantidad < 0:
                        print("Cantidad no valida, debe ser un numero positivo")
                        continue
                    break
                libros_service.actualizar_stock(isbn,-cantidad)
                
                

        elif (opcion == "14"):
            salir = False
            op = int(input("Agregar(1) | Eliminar(2) : " ))
            if(op==1):
                while(True):
                    while (True):
                        isbn = input("Escribe el isbn del libro: ").upper()
                        if isbn[:5] != "ISBN-":
                            print("Debes iniciar con 'ISBN-' ")
                            continue
                        break
                    titulo = input("Escribe el titulo del libro: ")
                    codigo_autor = input("Escribe el codigo del autor del libro: ")
                    autor = autores_service.buscar_por_codigo(codigo_autor)
                    if autor is None:
                        opp = input("¿Desea registrar un nuevo autor (1) o intentar de nuevo con uno ya registrado (2)?: ")
                        if (opp == "1"):
                            while(True):
                                codigo_autor = input("Ingrese codigo del autor a registrar: ")
                                nombre_autor = input("Ingrese nombre del autor a registrar: ")
                                email_autor = input("Ingrese email del autor a registrar: ")
                                autor = autores_service.registrar_autor(codigo_autor,nombre_autor,email_autor)
                                if autor is None:
                                    continue
                        elif (opp == "2"):
                            continue
                    stock = int(input("Escriba el stock: "))
                    categoria = input("Escribe la categoria: ")
                    if(autor is not None):
                        break
                libro_nuevo = libros_service.registrar_libro(isbn,titulo,autor.codigo,categoria,stock)
                
            elif (op == 2):
                isbn = input("Ingrese el isbn del libro a eliminar: ").upper()
                libros_service.eliminar_libro(isbn)
            else: 
                print("Opccion incorrecta")

        elif (opcion == "15"):
            nombre = input("Ingrese nombre del bibliotecario (Apellidos, Nombre): ")
            while(True):
                codigo = input("Escriba su codigo con la B delante: ").upper()
                if (codigo[0] != "B"):
                    print("Codigo no valido, debe empezar con B")
                    continue
                if (len(codigo) != 10):
                    print("Codigo no valido, debe tener 10 caracteres")
                    continue
                break
            email = input("Ingrese su correo electronico: ")
            nivel_acceso = 1
            bibliotecario = bibliotecarios_service.registrar_bibliotecario(nombre,codigo,email,nivel_acceso)
            print(f"Registrado: {bibliotecario.nombre} ")
        elif (opcion == "16"):
            while(True):
                codigo = input("Ingrese el codigo del bibliotecario a eliminar: ").upper()
                if codigo[0] != "B":
                    print("Debe iniciar con B")
                    continue    
                if len(codigo) != 10:
                    print("Tu codigo debe de tener 10 digitos")  
                    continue
                break
            bibliotecarios_service.eliminar_bibliotecario(codigo)

        elif (opcion == "0"):
            print(f"Hasta pronto, {usuario.nombre}!")
            break
        
        else:
            print("Opción invalida")

if __name__ == "__main__":
    main()