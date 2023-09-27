import csv

# Datos de ejemplo para hoteles y reservas
datos_hoteles = [
    {"nombre": "LidoHotel", "direccion": "Mañongo, Valencia", "telefono": "+58-4120908914"},
    {"nombre": "Hesperia", "direccion": "Mañongo, Valencia", "telefono": "+58-4248348756"}
]

datos_reservas = [
    {"id_hotel": 0, "nombre_cliente": "Juan", "id_habitacion": "101", "check_in": "24/08/2023", "check_out": "27/08/2023"},
    {"id_hotel": 1, "nombre_cliente": "Maria", "id_habitacion": "171", "check_in": "12/09/2023", "check_out": "15/09/2023"},
    {"id_hotel": 0, "nombre_cliente": "Pedro", "id_habitacion": "201", "check_in": "18/09/2023", "check_out": "20/09/2023"},
    {"id_hotel": 1, "nombre_cliente": "José", "id_habitacion": "202", "check_in": "22/09/2023", "check_out": "25/09/2023"}
]

# Guardar datos de hoteles en hoteles.csv
with open('hoteles.csv', 'w', newline='') as archivo_csv:
    campos = ["nombre", "direccion", "telefono"]
    writer = csv.DictWriter(archivo_csv, fieldnames=campos)
    writer.writeheader()
    writer.writerows(datos_hoteles)

# Guardar datos de reservas en reservas.csv
with open('reservas.csv', 'w', newline='') as archivo_csv:
    campos = ["id_hotel", "nombre_cliente", "id_habitacion", "check_in", "check_out"]
    writer = csv.DictWriter(archivo_csv, fieldnames=campos)
    writer.writeheader()
    writer.writerows(datos_reservas)

print("Archivos CSV creados con datos predeterminados.")
