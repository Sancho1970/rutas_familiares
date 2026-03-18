# Rutas Familiares

Herramienta para generar rutas personalizadas en familia usando la API de Google Maps. Ideal para encontrar parques, restaurantes o lugares de interés cercanos a una ubicación.

## 📌 Requisitos
- **Python 3.11** (entorno virtual recomendado).
- **Dependencias**: `googlemaps`, `folium`, `geopy`, `pandas`, `python-dotenv`.
- **Clave de API**: Google Places API Key (configurada en `.env`).

## 🛠️ Instalación
1. **Clonar el repositorio** (o descargar el proyecto):
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd rutas_familiares
   ```

2. **Crear y activar un entorno virtual** (opcional pero recomendado):
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la clave de API**:
   - Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
     ```
     GOOGLE_PLACES_API_KEY=TU_CLAVE_DE_API_AQUI
     ```

## 🚀 Uso
1. **Ejecutar el script**:
   ```bash
   python3 ruta_familiar.py
   ```

2. **Seleccionar una opción**:
   - `1`: Usar ubicación actual (GPS).
   - `2`: Introducir ubicación manualmente (ej: "Madrid, España").

3. **Especificar preferencias**:
   - Tipo de lugar (ej: `park`, `restaurant`, `museum`).
   - Radio de búsqueda (en metros).

4. **Resultado**:
   - Se generará un archivo HTML (`rutas_generadas/ruta_<tipo>_<fecha>.html`) con el mapa interactivo.
   - Abre el archivo en un navegador para ver la ruta.

## 📂 Estructura del proyecto
```
rutas_familiares/
├── config.py            # Configuración del proyecto
├── .env                 # Variables de entorno (clave API)
├── requirements.txt     # Dependencias
├── ruta_familiar.py     # Script principal
├── rutas_generadas/     # Mapas generados (HTML)
└── README.md            # Documentación
```

## 📝 Ejemplo de salida
![Ejemplo de mapa generado](https://i.imgur.com/ejemplo_mapa.png)
*(Mapa interactivo con marcadores de lugares cercanos).*

## ⚠️ Notas
- **Ubicación actual**: Requiere acceso a GPS o IP geolocalizada.
- **Clave de API**: Asegúrate de que la clave tenga permisos para **Google Places API**.
- **Límites de la API**: Google Places tiene un límite de solicitudes gratuitas (ver [documentación](https://developers.google.com/maps/documentation/places/web-service/usage-and-billing)).

## 📌 TODO
- [ ] Añadir más tipos de lugares (ej: farmacias, supermercados).
- [ ] Implementar guardado de rutas favoritas.
- [ ] Mejorar la interfaz de usuario (CLI o web).