# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 23:21:37 2024
Estadistica descriptiva teste

@author: VFox
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def seleccionar_archivo():
    global archivo_path, df
    archivo_path = filedialog.askopenfilename()
    if archivo_path:
        df = pd.read_csv(archivo_path)
        actualizar_listbox(df.columns)
        lbl_estado.config(text="Archivo seleccionado: " + archivo_path)

def actualizar_listbox(columnas):
    listbox.delete(0, tk.END)
    for col in columnas:
        listbox.insert(tk.END, col)
    lbl_estado.config(text="Seleccione las columnas para generar estadísticas")

def guardar_archivo(extension, sugerido):
    archivo = filedialog.asksaveasfilename(defaultextension=extension, initialfile=sugerido, filetypes=[(extension.upper() + " files", "*" + extension), ("All files", "*.*")])
    return archivo

def generar_estadisticas():
    seleccionadas = [listbox.get(i) for i in listbox.curselection()]
    if not seleccionadas:
        messagebox.showwarning("Advertencia", "Debe seleccionar al menos una columna")
        return
    datos = df[seleccionadas]
    
    # Estadísticas descriptivas
    estadisticas = datos.describe()
    archivo_csv = guardar_archivo(".csv", "estadisticas_descriptivas")
    if archivo_csv:
        estadisticas.to_csv(archivo_csv, index=True)  # Aseguramos que el índice se guarde en el CSV
        lbl_estado.config(text="Estadísticas guardadas en " + archivo_csv)

def generar_graficos():
    seleccionadas = [listbox.get(i) for i in listbox.curselection()]
    if not seleccionadas:
        messagebox.showwarning("Advertencia", "Debe seleccionar al menos una columna")
        return
    datos = df[seleccionadas]
    
    # Gráficos
    for col in seleccionadas:
        if pd.api.types.is_numeric_dtype(datos[col]):
            plt.figure()
            sns.histplot(datos[col], kde=True)
            plt.title(f'Histograma de {col}')
            archivo_histograma = guardar_archivo(".jpg", f'histograma_{col}')
            if archivo_histograma:
                plt.savefig(archivo_histograma)
            
            plt.figure()
            sns.boxplot(x=datos[col])
            plt.title(f'Boxplot de {col}')
            archivo_boxplot = guardar_archivo(".jpg", f'boxplot_{col}')
            if archivo_boxplot:
                plt.savefig(archivo_boxplot)

    lbl_estado.config(text="Gráficos generados con éxito")

def salir():
    root.quit()

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Estadísticas Descriptivas CSV")
root.geometry("400x600")

# Añadir logo con tamaño definido
logo_path = "fox1.png"
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((150, 150), Image.ANTIALIAS)  # Ajusta la imagen al tamaño deseado
logo = ImageTk.PhotoImage(logo_img)
lbl_logo = tk.Label(root, image=logo)
lbl_logo.pack(pady=10)

lbl_instrucciones = tk.Label(root, text="1. Seleccione un archivo CSV\n2. Seleccione las columnas\n3. Genere las estadísticas y gráficos")
lbl_instrucciones.pack(pady=10)

btn_seleccionar = tk.Button(root, text="Seleccionar Archivo CSV", command=seleccionar_archivo)
btn_seleccionar.pack(pady=20)

listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
listbox.pack(pady=20)

btn_estadisticas = tk.Button(root, text="Generar Estadísticas", command=generar_estadisticas)
btn_estadisticas.pack(pady=10)

btn_graficos = tk.Button(root, text="Generar Gráficos", command=generar_graficos)
btn_graficos.pack(pady=10)

btn_salir = tk.Button(root, text="Salir", command=salir)
btn_salir.pack(pady=20)

lbl_estado = tk.Label(root, text="Estado: Esperando que seleccione un archivo")
lbl_estado.pack(pady=10)

root.mainloop()
