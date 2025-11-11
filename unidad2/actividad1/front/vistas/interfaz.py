import tkinter as tk
from controladores.comunicacion import Comunicacion
from modelos.usuario import Usuario

class Interfaz():

    def __init__(self):
        self.ventanaPrincipal = tk.Tk()
        self.comunicacion = Comunicacion(self.ventanaPrincipal)
        pass

    def accion_guardar_boton(self, tema, descripcion, numero):
        self.comunicacion.guardar(tema, descripcion, numero)

    def accion_consultar_boton(self, labelConsulta, id):
        resultado = self.comunicacion.consultar(id)
        labelConsulta.config(text = resultado.get('numero_clase'))

    def accion_consultar_todo(self, tema, descripcion, numero):
        resultado = self.comunicacion.consultarTodo(tema, descripcion, numero)
        print(resultado)

    def mostrar_interfaz(self):

        usuario = Usuario(self.ventanaPrincipal)

        labelTema = tk.Label(self.ventanaPrincipal, text="Tema")
        entryTema = tk.Entry(self.ventanaPrincipal, textvariable=usuario.tema)
        labelDescripcion = tk.Label(self.ventanaPrincipal, text="Descripcion")
        entryDescripcion = tk.Entry(self.ventanaPrincipal, textvariable=usuario.descripcion)
        labelNumero = tk.Label(self.ventanaPrincipal, text="Número de clase")
        entryNumero = tk.Entry(self.ventanaPrincipal, textvariable=usuario.numero_clase)
        labelConsulta = tk.Label(self.ventanaPrincipal, text='')
        
        boton_guardar = tk.Button(self.ventanaPrincipal, 
                   text="Guardar", 
                   command=lambda: self.accion_guardar_boton(entryTema.get(), entryDescripcion.get(), entryNumero.get()))
        
        boton_consultar_1 = tk.Button(self.ventanaPrincipal, 
                   text="Consultar 1", 
                   command=lambda: self.accion_consultar_boton(labelConsulta, entryNumero.get()))
        
        boton_consultar_todos = tk.Button(self.ventanaPrincipal, 
                   text="Consultar todos", 
                   command=lambda: self.accion_consultar_todo(entryTema.get(), entryDescripcion.get(), entryNumero.get()))

        #creando la ventana
        self.ventanaPrincipal.title("Ventana Principal")
        self.ventanaPrincipal.geometry("300x300")
        labelTema.pack()
        entryTema.pack()
        labelDescripcion.pack()
        entryDescripcion.pack()
        labelNumero.pack()
        entryNumero.pack()
        boton_guardar.pack()
        boton_consultar_1.pack()
        boton_consultar_todos.pack()
        labelConsulta.pack()

        self.ventanaPrincipal.mainloop()