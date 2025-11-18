"""
1) Mezclador de tareas simples (threading directo)
Objetivo: practicar creación de hilos, start() y join() con funciones y argumentos.
Enunciado: crea 3 hilos que ejecuten funciones simples y de distinta duración (simuladas
con sleep).
Cada función imprime su inicio y fin. No uses Event, Lock, Queue ni daemon.
"""
import threading
import time

def tarea (hilo, duracion):
    print(f"Inicio de la tarea {hilo}")
    time.sleep(duracion)  
    print(f"Fin de la tarea {hilo}")

def main():
    hilo1 = threading.Thread(target=tarea, args=("hilo 1", 1.2))
    hilo2 = threading.Thread(target=tarea, args=("hilo 2", 2.9))
    hilo3 = threading.Thread(target=tarea, args=("hilo 3", 1.6))
    hilo4 = threading.Thread(target=tarea, args=("hilo 4", 2.0))


    hilo1.start()
    hilo2.start()
    hilo3.start()
    hilo4.start()

    hilo1.join()
    hilo2.join()
    hilo3.join()
    hilo4.join()

    print("finalizaron todas las tareas")

if __name__ == "__main__":
    main()