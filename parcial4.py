import csv
import json

class Hotel:
    def __init__(self, nombre, direccion, telefono):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.habitaciones = []
        self.reservas = []

    def agregar_habitacion(self, habitacion):
        self.habitaciones.append(habitacion)

    def modificar_habitacion(self, id_habitacion, nuevos_detalles):
        for habitacion in self.habitaciones:
            if habitacion['id'] == id_habitacion:
                habitacion.update(nuevos_detalles)
                break

    def listar_habitaciones(self):
        return self.habitaciones

    def crear_reserva(self, reserva):
        self.reservas.append(reserva)

    def eliminar_reserva(self, id_reserva):
        for reserva in self.reservas:
            if reserva['id'] == id_reserva:
                self.reservas.remove(reserva)
                break

    def listar_reservas(self):
        return self.reservas

    def buscar_reserva(self, consulta):
        resultados = []
        for reserva in self.reservas:
            if consulta in reserva['nombre_cliente']:
                resultados.append(reserva)
        return resultados

class Reserva:
    def __init__(self, nombre_cliente, id_habitacion, check_in, check_out):
        self.nombre_cliente = nombre_cliente
        self.id_habitacion = id_habitacion
        self.check_in = check_in
        self.check_out = check_out
        self.estado = "Activa"

class HistorialAcciones:
    def __init__(self):
        self.historial = []

    def registrar_accion(self, tipo_accion, detalles):
        self.historial.append({"tipo": tipo_accion, "detalles": detalles})

    def registrar_error(self, mensaje_error):
        self.historial.append({"tipo": "Error", "detalles": mensaje_error})

class GestorArchivos:
    @staticmethod
    def guardar_datos_en_csv(filename, datos):
        with open(filename, 'w', newline='') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=datos[0].keys())
            writer.writeheader()
            writer.writerows(datos)

    @staticmethod
    def cargar_datos_desde_csv(filename):
        try:
            with open(filename, 'r', newline='') as archivo_csv:
                reader = csv.DictReader(archivo_csv)
                datos = [fila for fila in reader]
                return datos
        except FileNotFoundError:
            return []

def cargar_datos():
    hoteles_data = GestorArchivos.cargar_datos_desde_csv('hoteles.csv')
    reservas_data = GestorArchivos.cargar_datos_desde_csv('reservas.csv')

    hoteles = []
    for hotel_data in hoteles_data:
        hotel = Hotel(hotel_data['nombre'], hotel_data['direccion'], hotel_data['telefono'])
        hoteles.append(hotel)

    for reserva_data in reservas_data:
        for hotel in hoteles:
            if int(reserva_data['id_hotel']) == hoteles.index(hotel):
                reserva = Reserva(
                    reserva_data['nombre_cliente'],
                    reserva_data['id_habitacion'],
                    reserva_data['check_in'],
                    reserva_data['check_out']
                )
                hotel.crear_reserva(reserva)

    return hoteles

def guardar_datos(hoteles):
    hoteles_data = []
    reservas_data = []

    for hotel in hoteles:
        hotel_data = {
            'nombre': hotel.nombre,
            'direccion': hotel.direccion,
            'telefono': hotel.telefono
        }
        hoteles_data.append(hotel_data)

        for reserva in hotel.reservas:
            reserva_data = {
                'id_hotel': hoteles.index(hotel),
                'nombre_cliente': reserva.nombre_cliente,
                'id_habitacion': reserva.id_habitacion,
                'check_in': reserva.check_in,
                'check_out': reserva.check_out
            }
            reservas_data.append(reserva_data)

    GestorArchivos.guardar_datos_en_csv('hoteles.csv', hoteles_data)
    GestorArchivos.guardar_datos_en_csv('reservas.csv', reservas_data)

def guardar_y_salir(hoteles):
    guardar_datos(hoteles)
    print("Datos guardados en archivos CSV. Saliendo del programa.")


if __name__ == "__main__":
    hoteles = cargar_datos()
    historial_acciones = HistorialAcciones()

    while True:
        print("\nSistema de Gestión de Reservaciones de Hoteles")
        print("1. Gestionar Hoteles")
        print("2. Gestionar Reservaciones")
        print("3. Historial de Acciones y Errores")
        print("4. Guardar y Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            # Gestionar Hoteles
            print("\nGestionar Hoteles")
            print("1. Crear Hotel")
            print("2. Modificar Hotel")
            print("3. Listar Hoteles")
            print("4. Eliminar Hotel")
            print("5. Volver al menú principal")

            opcion_hotel = input("Seleccione una opción: ")

            if opcion_hotel == "1":
                # Crear Hotel
                nombre = input("Nombre del hotel: ")
                direccion = input("Dirección del hotel: ")
                telefono = input("Número de teléfono del hotel: ")
                hotel = Hotel(nombre, direccion, telefono)
                hoteles.append(hotel)
                historial_acciones.registrar_accion("Crear Hotel", f"Nombre: {nombre}, Dirección: {direccion}, Teléfono: {telefono}")
                print("Hotel creado con éxito.")

            elif opcion_hotel == "2":
                # Modificar Hotel
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion = int(input("Seleccione el número de hotel a modificar: ")) 
                if seleccion >= 0 and seleccion < len(hoteles):
                    nombre_nuevo = input("Nuevo nombre (dejar en blanco para no cambiar): ")
                    direccion_nueva = input("Nueva dirección (dejar en blanco para no cambiar): ")
                    telefono_nuevo = input("Nuevo teléfono (dejar en blanco para no cambiar): ")

                    detalles_modificados = []
                    if nombre_nuevo:
                        detalles_modificados.append(f"Nombre: {nombre_nuevo}")
                        hoteles[seleccion].nombre = nombre_nuevo
                    if direccion_nueva:
                        detalles_modificados.append(f"Dirección: {direccion_nueva}")
                        hoteles[seleccion].direccion = direccion_nueva
                    if telefono_nuevo:
                        detalles_modificados.append(f"Teléfono: {telefono_nuevo}")
                        hoteles[seleccion].telefono = telefono_nuevo

                    historial_acciones.registrar_accion("Modificar Hotel", f"Hotel: {hoteles[seleccion].nombre}, Detalles Modificados: {', '.join(detalles_modificados)}")
                    print("Hotel modificado con éxito.")

                else:
                    print("Selección no válida.")

            elif opcion_hotel == "3":
                # Listar Hoteles
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. Nombre: {hotel.nombre}, Dirección: {hotel.direccion}, Teléfono: {hotel.telefono}")

            elif opcion_hotel == "4":
                # Eliminar Hotel
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion = int(input("Seleccione el número de hotel a eliminar: ")) - 1
                if seleccion >= 0 and seleccion < len(hoteles):
                    historial_acciones.registrar_accion("Eliminar Hotel", f"Nombre: {hoteles[seleccion].nombre}")
                    del hoteles[seleccion]
                    print("Hotel eliminado con éxito.")
                else:
                    print("Selección no válida.")

            elif opcion_hotel == "5":
                continue

            else:
                print("Opción no válida. Intente nuevamente.")

        elif opcion == "2":
            # Gestionar Reservaciones
            print("\nGestionar Reservaciones")
            print("1. Crear Reserva")
            print("2. Eliminar Reserva")
            print("3. Listar Reservas")
            print("4. Buscar Reservas")
            print("5. Volver al menú principal")

            opcion_reserva = input("Seleccione una opción: ")

            if opcion_reserva == "1":
                # Crear Reserva
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion_hotel = int(input("Seleccione el número de hotel: ")) - 1
                if seleccion_hotel >= 0 and seleccion_hotel < len(hoteles):
                    nombre_cliente = input("Nombre del cliente: ")
                    id_habitacion = input("ID de la habitación: ")
                    check_in = input("Fecha de check-in (DD/MM/AAAA): ")
                    check_out = input("Fecha de check-out (DD/MM/AAAA): ")

                    reserva = Reserva(nombre_cliente, id_habitacion, check_in, check_out)
                    hoteles[seleccion_hotel].crear_reserva(reserva)
                    historial_acciones.registrar_accion("Crear Reserva", f"Hotel: {hoteles[seleccion_hotel].nombre}, Cliente: {nombre_cliente}, Habitación: {id_habitacion}, Check-in: {check_in}, Check-out: {check_out}")
                    print("Reserva creada con éxito.")
                else:
                    print("Selección de hotel no válida.")

            elif opcion_reserva == "2":
                # Eliminar Reserva
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion_hotel = int(input("Seleccione el número de hotel: ")) - 1
                if seleccion_hotel >= 0 and seleccion_hotel < len(hoteles):
                    print("\nLista de Reservas:")
                    for i, reserva in enumerate(hoteles[seleccion_hotel].reservas):
                        print(f"{i + 1}. Cliente: {reserva.nombre_cliente}, Habitación: {reserva.id_habitacion}, Check-in: {reserva.check_in}, Check-out: {reserva.check_out}")

                    seleccion_reserva = int(input("Seleccione el número de reserva a eliminar: ")) - 1
                    if seleccion_reserva >= 0 and seleccion_reserva < len(hoteles[seleccion_hotel].reservas):
                        reserva_eliminada = hoteles[seleccion_hotel].reservas.pop(seleccion_reserva)
                        historial_acciones.registrar_accion("Eliminar Reserva", f"Hotel: {hoteles[seleccion_hotel].nombre}, Cliente: {reserva_eliminada.nombre_cliente}, Habitación: {reserva_eliminada.id_habitacion}, Check-in: {reserva_eliminada.check_in}, Check-out: {reserva_eliminada.check_out}")
                        print("Reserva eliminada con éxito.")
                    else:
                        print("Selección de reserva no válida.")
                else:
                    print("Selección de hotel no válida.")

            elif opcion_reserva == "3":
                # Listar Reservas
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion_hotel = int(input("Seleccione el número de hotel: ")) - 1
                if seleccion_hotel >= 0 and seleccion_hotel < len(hoteles):
                    print("\nLista de Reservas:")
                    for i, reserva in enumerate(hoteles[seleccion_hotel].reservas):
                        print(f"{i + 1}. Cliente: {reserva.nombre_cliente}, Habitación: {reserva.id_habitacion}, Check-in: {reserva.check_in}, Check-out: {reserva.check_out}")
                else:
                    print("Selección de hotel no válida.")

            elif opcion_reserva == "4":
                # Buscar Reservas
                print("\nLista de Hoteles:")
                for i, hotel in enumerate(hoteles):
                    print(f"{i + 1}. {hotel.nombre}")

                seleccion_hotel = int(input("Seleccione el número de hotel: ")) - 1
                if seleccion_hotel >= 0 and seleccion_hotel < len(hoteles):
                    consulta = input("Ingrese el nombre del cliente a buscar: ")
                    resultados = hoteles[seleccion_hotel].buscar_reserva(consulta)
                    if resultados:
                        print("\nResultados de la búsqueda:")
                        for i, reserva in enumerate(resultados):
                            print(f"{i + 1}. Cliente: {reserva.nombre_cliente}, Habitación: {reserva.id_habitacion}, Check-in: {reserva.check_in}, Check-out: {reserva.check_out}")
                    else:
                        print("No se encontraron reservas para el cliente especificado.")
                else:
                    print("Selección de hotel no válida.")

            elif opcion_reserva == "5":
                continue

            else:
                print("Opción no válida. Intente nuevamente.")

        elif opcion == "3":
            # Historial de Acciones y Errores
            print("\nHistorial de Acciones y Errores:")
            for i, accion in enumerate(historial_acciones.historial):
                print(f"{i + 1}. Tipo: {accion['tipo']}, Detalles: {accion['detalles']}")

        elif opcion == "4":
            guardar_y_salir(hoteles)
            break

        else:
            print("Opción no válida. Intente nuevamente.")
