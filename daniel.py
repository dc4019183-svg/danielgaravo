# Autor: Daniel Garavito

libros = []
usuarios = []
prestamos = []

MULTA_POR_DIA = 1000


def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()

        if texto == "":
            print("Error: este dato no puede quedar vacio.")
        else:
            return texto


def pedir_entero(mensaje, minimo=0):
    while True:
        try:
            numero = int(input(mensaje).strip())

            if numero < minimo:
                print("Error: el numero debe ser mayor o igual a", minimo)
            else:
                return numero

        except ValueError:
            print("Error: debes escribir un numero entero.")


def buscar_libro(codigo):
    for libro in libros:
        if libro["codigo"].lower() == codigo.lower():
            return libro

    return None


def buscar_usuario(documento):
    for usuario in usuarios:
        if usuario["documento"].lower() == documento.lower():
            return usuario

    return None


def buscar_prestamo(codigo_libro):
    for prestamo in prestamos:
        if prestamo["codigo_libro"].lower() == codigo_libro.lower():
            return prestamo

    return None


def registrar_libro():
    print("\n--- REGISTRAR LIBRO ---")

    codigo = pedir_texto("Codigo del libro: ")

    if buscar_libro(codigo) is not None:
        print("Ya existe un libro con ese codigo.")
        return

    titulo = pedir_texto("Titulo del libro: ")
    autor = pedir_texto("Autor del libro: ")

    nuevo_libro = {
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "disponible": True
    }

    libros.append(nuevo_libro)
    print("Libro registrado correctamente.")


def registrar_usuario():
    print("\n--- REGISTRAR USUARIO ---")

    documento = pedir_texto("Documento del usuario: ")

    if buscar_usuario(documento) is not None:
        print("Ya existe un usuario con ese documento.")
        return

    nombre = pedir_texto("Nombre completo: ")
    telefono = pedir_texto("Telefono: ")

    nuevo_usuario = {
        "documento": documento,
        "nombre": nombre,
        "telefono": telefono
    }

    usuarios.append(nuevo_usuario)
    print("Usuario registrado correctamente.")


def listar_libros():
    print("\n--- LISTA DE LIBROS ---")

    if len(libros) == 0:
        print("Todavia no hay libros registrados.")
        return

    for posicion in range(len(libros)):
        libro = libros[posicion]

        if libro["disponible"]:
            estado = "Disponible"
        else:
            estado = "Prestado"

        print("\nLibro numero:", posicion + 1)
        print("Codigo:", libro["codigo"])
        print("Titulo:", libro["titulo"])
        print("Autor:", libro["autor"])
        print("Estado:", estado)


def listar_usuarios():
    print("\n--- LISTA DE USUARIOS ---")

    if len(usuarios) == 0:
        print("Todavia no hay usuarios registrados.")
        return

    for posicion in range(len(usuarios)):
        usuario = usuarios[posicion]

        print("\nUsuario numero:", posicion + 1)
        print("Documento:", usuario["documento"])
        print("Nombre:", usuario["nombre"])
        print("Telefono:", usuario["telefono"])


def prestar_libro():
    print("\n--- PRESTAR LIBRO ---")

    if len(libros) == 0:
        print("Primero debes registrar por lo menos un libro.")
        return

    if len(usuarios) == 0:
        print("Primero debes registrar por lo menos un usuario.")
        return

    codigo = pedir_texto("Codigo del libro: ")
    libro = buscar_libro(codigo)

    if libro is None:
        print("No se encontro un libro con ese codigo.")
        return

    if not libro["disponible"]:
        print("Ese libro ya se encuentra prestado.")
        return

    documento = pedir_texto("Documento del usuario: ")
    usuario = buscar_usuario(documento)

    if usuario is None:
        print("No se encontro un usuario con ese documento.")
        return

    dias_prestamo = pedir_entero(
        "Cantidad de dias permitidos para devolverlo: ", 1
    )

    nuevo_prestamo = {
        "codigo_libro": libro["codigo"],
        "documento_usuario": usuario["documento"],
        "dias_permitidos": dias_prestamo
    }

    prestamos.append(nuevo_prestamo)
    libro["disponible"] = False

    print("Prestamo registrado correctamente.")
    print("El libro fue prestado a:", usuario["nombre"])
    print("Debe devolverlo en", dias_prestamo, "dia(s).")


def devolver_libro():
    print("\n--- DEVOLVER LIBRO ---")

    if len(prestamos) == 0:
        print("No hay prestamos activos.")
        return

    codigo = pedir_texto("Codigo del libro que se devuelve: ")
    prestamo = buscar_prestamo(codigo)

    if prestamo is None:
        print("Ese libro no aparece en los prestamos activos.")
        return

    libro = buscar_libro(prestamo["codigo_libro"])
    usuario = buscar_usuario(prestamo["documento_usuario"])

    dias_utilizados = pedir_entero(
        "Cuantos dias tuvo el usuario el libro: ", 0
    )

    dias_retraso = dias_utilizados - prestamo["dias_permitidos"]

    if dias_retraso > 0:
        multa = dias_retraso * MULTA_POR_DIA
        print("La devolucion tiene", dias_retraso, "dia(s) de retraso.")
        print("La multa es de $", multa)
    else:
        multa = 0
        print("El libro fue devuelto a tiempo. No tiene multa.")

    if libro is not None:
        libro["disponible"] = True

    prestamos.remove(prestamo)

    if usuario is not None:
        print("Devolucion registrada para:", usuario["nombre"])
    else:
        print("Devolucion registrada correctamente.")


def mostrar_prestamos():
    print("\n--- PRESTAMOS ACTIVOS ---")

    if len(prestamos) == 0:
        print("No hay prestamos activos.")
        return

    for posicion in range(len(prestamos)):
        prestamo = prestamos[posicion]
        libro = buscar_libro(prestamo["codigo_libro"])
        usuario = buscar_usuario(prestamo["documento_usuario"])

        print("\nPrestamo numero:", posicion + 1)

        if libro is not None:
            print("Libro:", libro["titulo"])
            print("Codigo:", libro["codigo"])
        else:
            print("Libro: informacion no disponible")

        if usuario is not None:
            print("Usuario:", usuario["nombre"])
            print("Documento:", usuario["documento"])
        else:
            print("Usuario: informacion no disponible")

        print("Dias permitidos:", prestamo["dias_permitidos"])


def mostrar_estadisticas():
    print("\n--- ESTADISTICAS ---")

    total_libros = len(libros)
    total_usuarios = len(usuarios)
    total_prestamos = len(prestamos)
    disponibles = 0

    for libro in libros:
        if libro["disponible"]:
            disponibles += 1

    prestados = total_libros - disponibles

    print("Libros registrados:", total_libros)
    print("Usuarios registrados:", total_usuarios)
    print("Libros disponibles:", disponibles)
    print("Libros prestados:", prestados)
    print("Prestamos activos:", total_prestamos)


def mostrar_menu():
    print("\n===================================")
    print("       BIBLIOTECA DEL BARRIO")
    print("===================================")
    print("1. Registrar libro")
    print("2. Registrar usuario")
    print("3. Listar libros")
    print("4. Listar usuarios")
    print("5. Prestar libro")
    print("6. Devolver libro")
    print("7. Mostrar prestamos activos")
    print("8. Mostrar estadisticas")
    print("9. Salir")
    print("===================================")


def ejecutar_programa():
    continuar = True

    while continuar:
        try:
            mostrar_menu()
            opcion = input("Selecciona una opcion: ").strip()

            if opcion == "1":
                registrar_libro()
            elif opcion == "2":
                registrar_usuario()
            elif opcion == "3":
                listar_libros()
            elif opcion == "4":
                listar_usuarios()
            elif opcion == "5":
                prestar_libro()
            elif opcion == "6":
                devolver_libro()
            elif opcion == "7":
                mostrar_prestamos()
            elif opcion == "8":
                mostrar_estadisticas()
            elif opcion == "9":
                continuar = False
                print("Programa finalizado. Hasta luego.")
            else:
                print("Opcion invalida. Escribe un numero del 1 al 9.")

        except (EOFError, KeyboardInterrupt):
            continuar = False
            print("\nPrograma finalizado.")

        except Exception as error:
            print("Ocurrio un error inesperado, pero el programa continuara.")
            print("Detalle del error:", str(error))


if __name__ == "__main__":
    ejecutar_programa()