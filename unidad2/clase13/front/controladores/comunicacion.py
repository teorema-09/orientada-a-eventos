import requests

class Comunicacion():

    def __init__(self, ventanaPrincipal):
        self.url = 'http://localhost:8000/v1/clase'
        self.ventanaPrincipal = ventanaPrincipal
        pass

    def guardar(self, tema, descripcion, numero_clase):
        try:
            print(tema, descripcion, numero_clase)
            data = {
                'tema': tema,
                'descripcion': descripcion,
                'numero_clase': int(numero_clase)
            }
            resultado = requests.post(self.url, json=data)
            print(resultado.json)
            return resultado
        except:
            pass
    
    def consultar(self, id):
        resultado = requests.get(self.url + '/' + str(id))
        return resultado.json()
    
    def consultarTodo(self, titulo, descripcion, numero):
        url = self.url
        
        print(url)
        resultado = requests.get(url)
        return resultado.json()