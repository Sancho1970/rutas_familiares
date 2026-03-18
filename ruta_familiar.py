#!/usr/bin/env python3
import os
import googlemaps
import folium
import pandas as pd
from geopy.distance import geodesic
from dotenv import load_dotenv
import webbrowser
from datetime import datetime

# Cargar API Key desde .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

# --- Funciones ---
def obtener_ubicacion_actual():
    """Obtener ubicación actual usando IP (aproximada) o GPS si está disponible."""
    print("Obteniendo ubicación actual...")
    # Nota: Para GPS real, necesitarías un módulo como `gpsd` o `geocoder`.
    # Aquí usamos una ubicación por defecto (Madrid) como ejemplo.
    return (40.416775, -3.703790)  # Latitud, Longitud (Madrid)

def buscar_lugares(tipo, ubicacion, radio=2000, min_calificacion=4.0):
    """Buscar lugares usando Google Places API."""
    print(f"Buscando {tipo} cerca de {ubicacion}...")
    lugares = gmaps.places_nearby(
        location=ubicacion,
        radius=radio,
        type=tipo,
        min_price=1,
        max_price=3,
        open_now=True
    )
    return lugares.get("results", [])

def filtrar_por_edad(lugares):
    """Filtrar lugares adecuados para niñas de 8 y 11 años."""
    lugares_filtrados = []
    for lugar in lugares:
        # Filtro básico: lugares con palabras clave en el nombre o tipos
        keywords = ["parque", "museo infantil", "zoo", "tienda de juguetes", "heladería", "librería infantil"]
        if any(keyword in lugar.get("name", "").lower() or keyword in lugar.get("types", []) for keyword in keywords):
            lugares_filtrados.append(lugar)
    return lugares_filtrados

def ordenar_por_cercania_y_calificacion(lugares, ubicacion):
    """Ordenar lugares por cercanía y calificación."""
    for lugar in lugares:
        lugar["distancia"] = geodesic(ubicacion, (lugar["geometry"]["location"]["lat"], lugar["geometry"]["location"]["lng"])).meters
    return sorted(lugares, key=lambda x: (x["distancia"], -x.get("rating", 0)))

def generar_mapa(lugares, ubicacion_inicial, nombre_archivo="ruta_familiar.html"):
    """Generar un mapa interactivo con Folium."""
    mapa = folium.Map(location=ubicacion_inicial, zoom_start=15)
    folium.Marker(
        location=ubicacion_inicial,
        popup="Ubicación actual",
        icon=folium.Icon(color="blue")
    ).add_to(mapa)

    for lugar in lugares:
        lat = lugar["geometry"]["location"]["lat"]
        lng = lugar["geometry"]["location"]["lng"]
        nombre = lugar["name"]
        calificacion = lugar.get("rating", "N/A")
        direccion = lugar.get("vicinity", "Dirección no disponible")
        popup_text = f"{nombre}<br>Calificación: {calificacion}<br>{direccion}"
        folium.Marker(
            location=(lat, lng),
            popup=popup_text,
            icon=folium.Icon(color="green")
        ).add_to(mapa)

    # Guardar mapa
    os.makedirs("rutas_generadas", exist_ok=True)
    ruta_archivo = f"rutas_generadas/{nombre_archivo}"
    mapa.save(ruta_archivo)
    print(f"Mapa generado: {ruta_archivo}")
    return ruta_archivo

def preguntar_preferencias():
    """Preguntar al usuario por sus preferencias."""
    print("\n--- Asistente de Rutas Familiares ---")
    print("1. Usar ubicación actual (GPS)")
    print("2. Introducir ubicación manualmente")
    opcion = input("Elige una opción (1/2): ")

    if opcion == "1":
        ubicacion = obtener_ubicacion_actual()
    elif opcion == "2":
        lat = float(input("Introduce latitud (ej: 40.416775): "))
        lng = float(input("Introduce longitud (ej: -3.703790): "))
        ubicacion = (lat, lng)
    else:
        print("Opción no válida. Usando ubicación por defecto (Madrid).")
        ubicacion = (40.416775, -3.703790)

    print("\n--- Tipos de lugares ---")
    print("1. Parques")
    print("2. Museos infantiles")
    print("3. Heladerías")
    print("4. Librerías infantiles")
    print("5. Zoológicos")
    tipo_opcion = input("Elige un tipo de lugar (1-5): ")
    tipos = {
        "1": "park",
        "2": "museum",
        "3": "cafe",  # Filtramos luego por "heladería"
        "4": "book_store",
        "5": "zoo"
    }
    tipo = tipos.get(tipo_opcion, "park")

    radio = int(input("Radio de búsqueda (en metros, ej: 2000): "))
    return ubicacion, tipo, radio

# --- Flujo principal ---
def main():
    ubicacion, tipo, radio = preguntar_preferencias()
    lugares = buscar_lugares(tipo, ubicacion, radio)
    lugares_filtrados = filtrar_por_edad(lugares)
    lugares_ordenados = ordenar_por_cercania_y_calificacion(lugares_filtrados, ubicacion)

    if not lugares_ordenados:
        print("No se encontraron lugares adecuados.")
        return

    print("\n--- Lugares recomendados ---")
    for i, lugar in enumerate(lugares_ordenados[:5], 1):  # Top 5
        print(f"{i}. {lugar['name']} (Calificación: {lugar.get('rating', 'N/A')}, Distancia: {lugar['distancia']:.0f}m)")

    nombre_archivo = f"ruta_familiar_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    ruta_mapa = generar_mapa(lugares_ordenados[:5], ubicacion, nombre_archivo)
    webbrowser.open(f"file://{os.path.abspath(ruta_mapa)}")

if __name__ == "__main__":
    main()
