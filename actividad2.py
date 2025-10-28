import tkinter as tk
from tkinter import messagebox
import re


RE_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")

RE_NUMEROS = re.compile(r"^\d+$")

def validar_letras(texto):
    return texto == "" or RE_LETRAS.match(texto)

def validar_numeros(texto):
    return texto == "" or RE_NUMEROS.match(texto)

ventana = tk.Tk()
ventana.title("Motocicleta")
ventana.geometry("400x370")
ventana.configure(bg="#e9ecef")
ventana.resizable(False, False)


var_Placa = tk.StringVar()
var_Propietario = tk.StringVar()
var_Cilindrage = tk.StringVar()
var_fecha_de_fabricacion = tk.StringVar()


err_Placa = tk.StringVar()
err_Propietario = tk.StringVar()
err_Cilindrage = tk.StringVar()
err_fecha_de_fabricacion = tk.StringVar()

def val_Placa(*_):
    txt = var_Placa.get()
    if validar_numeros(txt):
        err_Placa.set("")
        return True
    err_Placa.set("Solo números y letras")
    

def val_Propietario(*_):
    txt = var_Propietario.get()
    if validar_letras(txt):
        err_Propietario.set("")
        return True
    err_Propietario.set("Solo letras")
    return False

def val_Cilindrage(*_):
    txt = var_Cilindrage.get()
    if validar_numeros(txt):
        err_Cilindrage.set("")
        return True
    err_Cilindrage.set("Solo números")
    return False

def val_fecha_de_fabricacion(*_):
    txt = var_fecha_de_fabricacion.get()
    if validar_numeros(txt):
        err_fecha_de_fabricacion.set("")
        return True
    err_fecha_de_fabricacion.set("Solo números")
    return False

def guardar():
    ok = True
    if not val_Placa():
        ok = False
    if not val_Propietario():
        ok = False
    if not val_Cilindrage():
        ok = False
    if not val_fecha_de_fabricacion():
        ok = False
    if var_Placa.get().strip() == "":
        err_Placa.set("La Placa es obligatoria.")
        ok = False
    if var_Propietario.get().strip() == "":
        err_Propietario.set("El Propietario es obligatorio.")
        ok = False
    if var_Cilindrage.get().strip() == "":
        err_Cilindrage.set("El cilindrage  es obligatorio.")
        ok = False
    if var_fecha_de_fabricacion.get().strip() == "":
        err_fecha_de_fabricacion.set("La fecha de Fabricacion es obligatorio.")
        ok = False
    if not ok:
        messagebox.showerror("Errores de validación", "Por favor llenar todos los campos.")
        return
    messagebox.showinfo("Guardado", "Datos guardados correctamente.")

tk.Label(ventana, text="Motocicleta", font=("Arial", 18, "bold"), bg="#e9ecef", fg="#212529").grid(row=0, column=0, columnspan=2, pady=(18, 22), sticky="nsew")


tk.Label(ventana, text="Placa:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=1, column=0, padx=18, pady=6, sticky="ew")
entry_modelo = tk.Entry(ventana, width=26, textvariable=var_Placa, font=("Arial", 11))
entry_modelo.grid(row=1, column=1, padx=18, pady=6)
tk.Label(ventana, textvariable=err_Placa, fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=2, column=1, sticky="ew", padx=18)


tk.Label(ventana, text="Propietario:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=3, column=0, padx=18, pady=6, sticky="ew")
entry_marca = tk.Entry(ventana, width=26, textvariable=var_Propietario, font=("Arial", 11))
entry_marca.grid(row=3, column=1, padx=18, pady=6)
tk.Label(ventana, textvariable=err_Propietario, fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=4, column=1, sticky="ew", padx=18)


tk.Label(ventana, text="Cilindrage:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=5, column=0, padx=18, pady=6, sticky="ew")
entry_talla = tk.Entry(ventana, width=26, textvariable=var_Cilindrage, font=("Arial", 11))
entry_talla.grid(row=5, column=1, padx=18, pady=6)
tk.Label(ventana, textvariable=err_Cilindrage, fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=6, column=1, sticky="ew", padx=18)


tk.Label(ventana, text="Fecha de fabricación:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=7, column=0, padx=18, pady=6, sticky="ew")
entry_fecha = tk.Entry(ventana, width=26, textvariable=var_fecha_de_fabricacion, font=("Arial", 11))
entry_fecha.grid(row=7, column=1, padx=18, pady=6)
tk.Label(ventana, textvariable=err_fecha_de_fabricacion, fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=8, column=1, sticky="ew", padx=18)



# Botón de Validar
def validar_campos():
    ok = True
    if not val_Placa():
        ok = False
    if not val_Propietario():
        ok = False
    if not val_Cilindrage():
        ok = False
    if not val_fecha_de_fabricacion():
        ok = False
    if var_Placa.get().strip() == "":
        err_Placa.set("La Placa es obligatoria.")
        ok = False
    if var_Propietario.get().strip() == "":
        err_Propietario.set("El Propietario es obligatorio.")
        ok = False
    if var_Cilindrage.get().strip() == "":
        err_Cilindrage.set("El cilindrage es obligatorio.")
        ok = False
    if var_fecha_de_fabricacion.get().strip() == "":
        err_fecha_de_fabricacion.set("La fecha de Fabricacion es obligatorio.")
        ok = False
    if ok:
        messagebox.showinfo("Validación", "Todos los datos son válidos.")
    else:
        messagebox.showerror("Errores de validación", "Por favor corrija los errores antes de continuar.")
def el_usuario_qeuiere_salir():
    if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
        ventana.destroy()

tk.Button(ventana, text="Validar", width=16, command=validar_campos, bg="#198754", fg="white", font=("Arial", 11, "bold"), activebackground="#157347").grid(row=9, column=0, pady=16, padx=(18,6))
tk.Button(ventana, text="Guardar", width=16, command=guardar, bg="#0d6efd", fg="white", font=("Arial", 11, "bold"), activebackground="#0a58ca").grid(row=9, column=1, pady=16, padx=(6,18))


entry_modelo.bind("<KeyRelease>", val_Placa)
entry_marca.bind("<KeyRelease>", val_Propietario)
entry_talla.bind("<KeyRelease>", val_Cilindrage)
entry_fecha.bind("<KeyRelease>", val_fecha_de_fabricacion)

ventana.protocol("WM_DELETE_WINDOW", el_usuario_qeuiere_salir)
ventana.mainloop()


