"""
2) Temporizador con reinicio (clases + Event)
Versión similar con estructura distinta pero mismo objetivo.
"""
import threading
import time

class Temporizador(threading.Thread):
    #Hilo que cuenta segundos hasta un límite y puede reiniciarse con un evento.
    
    def __init__(self, limite, evento_reset, evento_stop):
        super().__init__()
        self.limite = limite
        self.evento_reset = evento_reset
        self.evento_stop = evento_stop

    def run(self):
        tiempo = 0
        print(f"Iniciando temporizador (límite: {self.limite}s)\n")
        while not self.evento_stop.is_set():
            print(f"Tiempo transcurrido: {tiempo}s")
            time.sleep(1)
            tiempo += 1

            
            if self.evento_reset.is_set():
                print("→ Reinicio detectado, contador a 0.\n")
                tiempo = 0
                self.evento_reset.clear()

            
            if tiempo >= self.limite:
                print(f"Tiempo límite alcanzado ({self.limite}s). Finalizando...\n")
                self.evento_stop.set()

class EscuchaReinicio(threading.Thread):
    """Hilo que espera la entrada del usuario para reiniciar el temporizador."""
    
    def __init__(self, evento_reset, evento_stop):
        super().__init__(daemon=True)
        self.evento_reset = evento_reset
        self.evento_stop = evento_stop

    def run(self):
        while not self.evento_stop.is_set():
            try:
                input("Presiona ENTER para reiniciar el temporizador...\n")
                if not self.evento_stop.is_set():
                    self.evento_reset.set()
            except KeyboardInterrupt:
                break

def main():
    print("=" * 60)
    print("Temporizador con reinicio manual")
    print("=" * 60)

    evento_reset = threading.Event()
    evento_stop = threading.Event()

    limite = 20
    temporizador = Temporizador(limite, evento_reset, evento_stop)
    escucha = EscuchaReinicio(evento_reset, evento_stop)

    escucha.start()
    temporizador.start()

    try:
        temporizador.join()
    except KeyboardInterrupt:
        print("\nDetención manual detectada.")
        evento_stop.set()
        temporizador.join(timeout=2)

    print(" Programa finalizado correctamente.")
    print("=" * 60)

if __name__ == "__main__":
    main()
