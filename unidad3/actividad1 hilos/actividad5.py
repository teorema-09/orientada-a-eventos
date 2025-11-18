"""
5) Logger en segundo plano (clases + daemon)
Objetivo: usar hilos daemon que no bloqueen el cierre del programa.
Enunciado: crea un LoggerDaemon que imprima mensajes periódicos de estado
y un hilo TrabajoPesado que simule una tarea principal.
El daemon se detiene automáticamente al terminar el programa.
"""
import threading
import time
import random

class LoggerDaemon(threading.Thread):
    def __init__(self, intervalo):
        super().__init__(daemon=True)  
        self.intervalo = intervalo

    def run(self):
        while True:
            print(f"[Logger] Sistema funcionando correctamente... ({time.strftime('%H:%M:%S')})")
            time.sleep(self.intervalo)


class TrabajoPesado(threading.Thread):
    def __init__(self, pasos):
        super().__init__()
        self.pasos = pasos

    def run(self):
        for i in range(1, self.pasos + 1):
            print(f"[TrabajoPesado] Ejecutando paso {i}/{self.pasos}...")
            time.sleep(random.uniform(1.0, 2.0))  # Simula proceso costoso
        print("[TrabajoPesado] Tarea principal completada.")


def main():
    # Crea un logger y la tarea principal
    logger = LoggerDaemon(intervalo=2)
    trabajo = TrabajoPesado(pasos=5)

    # Iniciar ambos hilos
    logger.start()
    trabajo.start()

    # Espera a que la tarea principal termine
    trabajo.join()

    print("\n[TODOS] El programa ha finalizado. El hilo daemon se cerrará automáticamente.\n")


if __name__ == "__main__":
    main()