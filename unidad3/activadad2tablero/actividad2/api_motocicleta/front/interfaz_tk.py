import tkinter as tk
from tkinter import ttk, messagebox
import re
import requests

API_URL = "http://127.0.0.1:8000/api/motocicletas/"

RE_LETRAS = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$")
RE_NUMEROS = re.compile(r"^\d+$")
RE_ALFANUM = re.compile(r"^[A-Za-z0-9]+$")

def validar_letras(texto): return texto == "" or bool(RE_LETRAS.match(texto))
def validar_numeros(texto): return texto == "" or bool(RE_NUMEROS.match(texto))
def validar_alfanum(texto): return texto == "" or bool(RE_ALFANUM.match(texto))

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Motocicleta")
    ventana.geometry("720x520")
    ventana.resizable(False, False)
    ventana.configure(bg="#e9ecef")

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
        ("fecha_fabricacion", validar_numeros, True, "La fecha de Fabricacion es obligatoria.", "Solo números"),
    ]

    def validar_campo(k):
        val = vars_[k].get().strip()
        validator = next(s[1] for s in esquema if s[0] == k)
        invalid_msg = next(s[4] for s in esquema if s[0] == k)
        errs[k].set("" if validator(val) else invalid_msg)
        return errs[k].get() == ""

    def validar_todos():
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
        for v in vars_.values(): v.set("")
        for e in errs.values(): e.set("")

    def load_data():
        try:
            r = requests.get(API_URL)
            return r.json() if r.status_code == 200 else []
        except: return []

    def refrescar_tabla():
        for row in tabla.get_children():
            tabla.delete(row)
        data = load_data()
        for m in data:
            tabla.insert("", "end", values=(
                m.get("placa"),
                m.get("propietario"),
                m.get("cilindrage"),
                m.get("fecha_fabricacion"),
            ))

    def on_select(event):
        sel = tabla.focus()
        if not sel: return
        vals = tabla.item(sel)["values"]
        if not vals: return
        vars_["placa"].set(vals[0])
        vars_["propietario"].set(vals[1])
        vars_["cilindrage"].set(vals[2])
        vars_["fecha_fabricacion"].set(vals[3])

    def guardar():
        if not validar_todos():
            messagebox.showerror("Errores", "Corrija los errores.")
            return

        payload = {
            "placa": vars_["placa"].get().strip(),
            "propietario": vars_["propietario"].get().strip(),
            "cilindrage": int(vars_["cilindrage"].get().strip()),
            "fecha_fabricacion": vars_["fecha_fabricacion"].get().strip(),
        }

        placa = payload["placa"]

        try:
            r = requests.get(f"{API_URL}{placa}/")
            if r.status_code == 200:
                if not messagebox.askyesno("Confirmar", "La placa ya existe. ¿Actualizar?"):
                    return
                r = requests.put(f"{API_URL}{placa}/", json=payload)
                if r.status_code == 200:
                    messagebox.showinfo("OK", "Actualizado.")
            else:
                r = requests.post(API_URL, json=payload)
                if r.status_code == 201:
                    messagebox.showinfo("OK", "Guardado.")
        except:
            messagebox.showerror("Error", "No se pudo conectar.")

        refrescar_tabla()

    def actualizar():
        if not validar_todos():
            messagebox.showerror("Errores", "Corrija los errores.")
            return

        placa = vars_["placa"].get().strip()
        payload = {
            "placa": placa,
            "propietario": vars_["propietario"].get().strip(),
            "cilindrage": int(vars_["cilindrage"].get().strip()),
            "fecha_fabricacion": vars_["fecha_fabricacion"].get().strip(),
        }

        try:
            r = requests.put(f"{API_URL}{placa}/", json=payload)
            if r.status_code == 200:
                messagebox.showinfo("OK", "Actualizado.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar.")
        except:
            messagebox.showerror("Error", "No hay conexión.")

        refrescar_tabla()

    def borrar():
        placa = vars_["placa"].get().strip()
        if placa == "":
            messagebox.showerror("Error", "Ingrese la placa.")
            return
        if not messagebox.askyesno("Confirmar", f"¿Borrar {placa}?"):
            return

        try:
            r = requests.delete(f"{API_URL}{placa}/")
            if r.status_code == 204:
                messagebox.showinfo("OK", "Eliminado.")
                limpiar_campos()
            else:
                messagebox.showerror("Error", "No se pudo eliminar.")
        except:
            messagebox.showerror("Error", "No hay conexión.")

        refrescar_tabla()

    tk.Label(ventana, text="Motocicleta", font=("Arial", 18, "bold"), bg="#e9ecef").grid(row=0, column=0, columnspan=2, pady=10)

    def campo(row, label, key):
        tk.Label(ventana, text=label, bg="#e9ecef").grid(row=row, column=0, padx=10, pady=2, sticky="w")
        ent = tk.Entry(ventana, textvariable=vars_[key], width=35)
        ent.grid(row=row, column=1, padx=10)
        tk.Label(ventana, textvariable=errs[key], fg="#c1121f", bg="#e9ecef", font=("Arial", 9)).grid(row=row+1, column=1, sticky="w")
        ent.bind("<KeyRelease>", lambda e, k=key: validar_campo(k))

    campo(1, "Placa:", "placa")
    campo(3, "Propietario:", "propietario")
    campo(5, "Cilindrage:", "cilindrage")
    campo(7, "Fecha fabricación:", "fecha_fabricacion")

    tk.Button(ventana, text="Guardar", width=15, command=guardar).grid(row=9, column=0, pady=10)
    tk.Button(ventana, text="Actualizar", width=15, command=actualizar).grid(row=9, column=1, pady=10)
    tk.Button(ventana, text="Borrar", width=15, command=borrar).grid(row=10, column=0, pady=6)
    tk.Button(ventana, text="Limpiar", width=15, command=limpiar_campos).grid(row=10, column=1, pady=6)

    frame_tabla = tk.Frame(ventana)
    frame_tabla.grid(row=11, column=0, columnspan=2, pady=10)

    tabla = ttk.Treeview(frame_tabla, columns=("placa", "propietario", "cilindrage", "fecha"), show="headings", height=8)
    tabla.heading("placa", text="Placa")
    tabla.heading("propietario", text="Propietario")
    tabla.heading("cilindrage", text="Cilindrage")
    tabla.heading("fecha", text="Fecha Fab.")

    tabla.column("placa", width=100)
    tabla.column("propietario", width=180)
    tabla.column("cilindrage", width=100)
    tabla.column("fecha", width=120)

    tabla.pack(side=tk.LEFT)
    tabla.bind("<<TreeviewSelect>>", on_select)

    scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    tabla.configure(yscrollcommand=scrollbar.set)

    refrescar_tabla()

    ventana.mainloop()

iniciar_interfaz()
