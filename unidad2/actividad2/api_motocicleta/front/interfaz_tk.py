import tkinter as tk
from tkinter import messagebox
import re
import requests

# API configuration
API_URL = "http://127.0.0.1:8000/api/motocicletas/"


RE_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")
RE_NUMEROS = re.compile(r"^\d+$")
RE_ALFANUM = re.compile(r"^[A-Za-z0-9]+$")


def validar_letras(texto):
    return texto == "" or bool(RE_LETRAS.match(texto))


def validar_numeros(texto):
    return texto == "" or bool(RE_NUMEROS.match(texto))


def validar_alfanum(texto):
    return texto == "" or bool(RE_ALFANUM.match(texto))


def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Motocicleta")
    ventana.geometry("480x420")
    ventana.configure(bg="#e9ecef")
    ventana.resizable(True, True)

    def load_data():
        """Carga todos los registros desde la API"""
        try:
            response = requests.get(API_URL)
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", f"Error al obtener datos de la API: {response.status_code}")
                return []
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar con la API: {str(e)}")
            return []

    vars_ = {
        "placa": tk.StringVar(),
        "propietario": tk.StringVar(),
        "cilindrage": tk.StringVar(),
        "fecha_fabricacion": tk.StringVar(),
    }
    errs = {k: tk.StringVar() for k in vars_}

  
    esquema = [
        ("placa", validar_alfanum, True, "La Placa es obligatoria.", "Solo números y letras (sin espacios)"),
        ("propietario", validar_letras, True, "El Propietario es obligatorio.", "Solo letras"),
        ("cilindrage", validar_numeros, True, "El cilindrage es obligatorio.", "Solo números"),
        ("fecha_fabricacion", validar_numeros, True, "La fecha de Fabricacion es obligatorio.", "Solo números"),
    ]

    def validar_campo(key):
        """Valida un campo según el esquema y actualiza su mensaje de error."""
        val = vars_[key].get().strip()
        validator = next(s[1] for s in esquema if s[0] == key)
        invalid_msg = next(s[4] for s in esquema if s[0] == key)
        errs[key].set("" if validator(val) else invalid_msg)
        return errs[key].get() == ""

    def validar_todos():
        """Valida todos los campos usando el esquema; devuelve True si todo OK."""
        ok = True
        for key, validator, required, req_msg, invalid_msg in esquema:
            txt = vars_[key].get().strip()
            if not validator(txt):
                errs[key].set(invalid_msg)
                ok = False
            elif required and txt == "":
                errs[key].set(req_msg)
                ok = False
            else:
                errs[key].set("")
        return ok

    def limpiar_campos():
        for v in vars_.values():
            v.set("")
        for e in errs.values():
            e.set("")

    def guardar():
        if not validar_todos():
            messagebox.showerror("Errores de validación", "Por favor llenar/corregir los campos.")
            return

        placa = vars_["placa"].get().strip()
        payload = {
            "placa": placa,
            "propietario": vars_["propietario"].get().strip(),
            "cilindrage": int(vars_["cilindrage"].get().strip()),
            "fecha_fabricacion": vars_["fecha_fabricacion"].get().strip(),
        }

        try:
            # Intentar obtener el registro existente
            response = requests.get(f"{API_URL}{placa}/")
            if response.status_code == 200:
                # Si existe, preguntar si desea actualizarlo
                if not messagebox.askyesno("Confirmar", "La placa ya existe. ¿Desea sobrescribirla?"):
                    return
                # Actualizar registro existente
                response = requests.put(f"{API_URL}{placa}/", json=payload)
                if response.status_code == 200:
                    messagebox.showinfo("Actualizado", "Registro actualizado correctamente.")
                else:
                    messagebox.showerror("Error", f"Error al actualizar: {response.status_code}")
            else:
                # Si no existe, crear nuevo registro
                response = requests.post(API_URL, json=payload)
                if response.status_code == 201:
                    messagebox.showinfo("Guardado", "Datos guardados correctamente.")
                else:
                    messagebox.showerror("Error", f"Error al guardar: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def consultar_todos():
        data = load_data()
        win = tk.Toplevel(ventana)
        win.title("Consultar todos")
        win.geometry("420x300")
        win.configure(bg="#f8f9fa")

        listbox = tk.Listbox(win, width=70, height=12)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=8, pady=8, expand=True)
        scrollbar = tk.Scrollbar(win, command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.config(yscrollcommand=scrollbar.set)

        if not data:
            listbox.insert(tk.END, "No hay registros guardados.")
        else:
            for rec in data:
                listbox.insert(
                    tk.END,
                    f"Placa: {rec.get('placa')} | Propietario: {rec.get('propietario')} | Cilindrage: {rec.get('cilindrage')} | Fecha: {rec.get('fecha_fabricacion')}",
                )

        tk.Button(win, text="Cerrar", command=win.destroy).pack(pady=(0, 8))

    def consultar_por_placa():
        placa = vars_["placa"].get().strip()
        if placa == "":
            messagebox.showerror("Error", "Ingrese la placa a consultar.")
            return
        
        try:
            response = requests.get(f"{API_URL}{placa}/")
            if response.status_code == 200:
                rec = response.json()
                for k in ("propietario", "cilindrage", "fecha_fabricacion"):
                    vars_[k].set(str(rec.get(k, "")))
                messagebox.showinfo("Encontrado", f"Registro cargado para placa {placa}.")
            else:
                messagebox.showerror("No encontrado", "No existe un registro con esa placa.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def actualizar():
        if not validar_todos():
            messagebox.showerror("Errores de validación", "Por favor llenar/corregir los campos.")
            return

        placa = vars_["placa"].get().strip()
        if placa == "":
            messagebox.showerror("Error", "Ingrese la placa a actualizar.")
            return

        payload = {
            "placa": placa,
            "propietario": vars_["propietario"].get().strip(),
            "cilindrage": int(vars_["cilindrage"].get().strip()),
            "fecha_fabricacion": vars_["fecha_fabricacion"].get().strip(),
        }

        try:
            response = requests.put(f"{API_URL}{placa}/", json=payload)
            if response.status_code == 200:
                messagebox.showinfo("Actualizado", "Registro actualizado correctamente.")
            else:
                messagebox.showerror("Error", f"No se pudo actualizar: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

    def borrar():
        placa = vars_["placa"].get().strip()
        if placa == "":
            messagebox.showerror("Error", "Ingrese la placa a borrar.")
            return
        if not messagebox.askyesno("Borrar", f"¿Seguro que desea borrar la placa {placa}?"):
            return

        try:
            response = requests.delete(f"{API_URL}{placa}/")
            if response.status_code == 204:
                limpiar_campos()
                messagebox.showinfo("Borrado", "Registro eliminado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el registro.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de conexión: {str(e)}")

   
    tk.Label(ventana, text="Motocicleta", font=("Arial", 18, "bold"), bg="#e9ecef", fg="#212529").grid(row=0, column=0, columnspan=2, pady=(18, 22), sticky="nsew")

    tk.Label(ventana, text="Placa:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=1, column=0, padx=18, pady=6, sticky="ew")
    entry_placa = tk.Entry(ventana, width=34, textvariable=vars_["placa"], font=("Arial", 11))
    entry_placa.grid(row=1, column=1, padx=18, pady=6)
    tk.Label(ventana, textvariable=errs["placa"], fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=2, column=1, sticky="ew", padx=18)

    tk.Label(ventana, text="Propietario:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=3, column=0, padx=18, pady=6, sticky="ew")
    entry_prop = tk.Entry(ventana, width=34, textvariable=vars_["propietario"], font=("Arial", 11))
    entry_prop.grid(row=3, column=1, padx=18, pady=6)
    tk.Label(ventana, textvariable=errs["propietario"], fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=4, column=1, sticky="ew", padx=18)

    tk.Label(ventana, text="Cilindrage:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=5, column=0, padx=18, pady=6, sticky="ew")
    entry_cili = tk.Entry(ventana, width=34, textvariable=vars_["cilindrage"], font=("Arial", 11))
    entry_cili.grid(row=5, column=1, padx=18, pady=6)
    tk.Label(ventana, textvariable=errs["cilindrage"], fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=6, column=1, sticky="ew", padx=18)

    tk.Label(ventana, text="Fecha de fabricación:", bg="#e9ecef", anchor="center", font=("Arial", 11)).grid(row=7, column=0, padx=18, pady=6, sticky="ew")
    entry_fecha = tk.Entry(ventana, width=34, textvariable=vars_["fecha_fabricacion"], font=("Arial", 11))
    entry_fecha.grid(row=7, column=1, padx=18, pady=6)
    tk.Label(ventana, textvariable=errs["fecha_fabricacion"], fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=8, column=1, sticky="ew", padx=18)


    tk.Button(ventana, text="Validar", width=16, command=lambda: messagebox.showinfo("Validación", "Todos los datos son válidos.") if validar_todos() else messagebox.showerror("Errores de validación", "Por favor corrija los errores."), bg="#198754", fg="white", font=("Arial", 11, "bold"), activebackground="#157347").grid(row=9, column=0, pady=12, padx=(18, 6))
    tk.Button(ventana, text="Guardar", width=16, command=guardar, bg="#0d6efd", fg="white", font=("Arial", 11, "bold"), activebackground="#0a58ca").grid(row=9, column=1, pady=12, padx=(6, 18))

  
    tk.Button(ventana, text="Consultar todos", width=16, command=consultar_todos, bg="#6c757d", fg="white", font=("Arial", 10)).grid(row=10, column=0, pady=6, padx=(18, 6))
    tk.Button(ventana, text="Consultar (placa)", width=16, command=consultar_por_placa, bg="#6c757d", fg="white", font=("Arial", 10)).grid(row=10, column=1, pady=6, padx=(6, 18))
    tk.Button(ventana, text="Actualizar", width=16, command=actualizar, bg="#0d6efd", fg="white", font=("Arial", 10)).grid(row=11, column=0, pady=6, padx=(18, 6))
    tk.Button(ventana, text="Borrar", width=16, command=borrar, bg="#dc3545", fg="white", font=("Arial", 10)).grid(row=11, column=1, pady=6, padx=(6, 18))
    tk.Button(ventana, text="Limpiar campos", width=34, command=limpiar_campos, bg="#adb5bd", fg="black", font=("Arial", 10)).grid(row=12, column=0, columnspan=2, pady=12, padx=18)

 
    entry_placa.bind("<KeyRelease>", lambda e: validar_campo("placa"))
    entry_prop.bind("<KeyRelease>", lambda e: validar_campo("propietario"))
    entry_cili.bind("<KeyRelease>", lambda e: validar_campo("cilindrage"))
    entry_fecha.bind("<KeyRelease>", lambda e: validar_campo("fecha_fabricacion"))

    def el_usuario_qeuiere_salir():
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            ventana.destroy()

    ventana.protocol("WM_DELETE_WINDOW", el_usuario_qeuiere_salir)
    ventana.mainloop()

