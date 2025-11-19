
import os
import sys
from interfaz_tk import iniciar_interfaz

def check_api_connection():
    import requests
    try:
        response = requests.get("http://127.0.0.1:8000/api/motocicletas/")
        if response.status_code == 200:
            print("Conexión exitosa con la API")
            return True
        else:
            print(f"Error al conectar con la API: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar con el servidor Django. Asegúrate de que esté corriendo.")
        return False



if __name__ == "__main__":
    if check_api_connection():
        iniciar_interfaz()
    else:
        print("No se puede iniciar la interfaz sin conexión a la API.")
        sys.exit(1)