import tkinter as tk
from tkinter import ttk, messagebox
import estructuras


# -------------------- FUNCIONES DEL MENU --------------------

def actualizar_tabla_productos():
    for fila in tabla_productos.get_children():
        tabla_productos.delete(fila)

    for indice, producto in enumerate(estructuras.productos):
        tabla_productos.insert(
            "", "end", iid=str(indice),
            values=(
                producto["nombre"],
                f'₡{producto["precio"]:,.2f}',
                producto["categoria"]
            )
        )

    estructuras.actualizar_cantidades()
    texto_categorias.config(
        text=(
            f"Comidas: {estructuras.cantidades[0]}  |  "
            f"Bebidas: {estructuras.cantidades[1]}  |  "
            f"Postres: {estructuras.cantidades[2]}"
        )
    )


def limpiar_campos_producto():
    entrada_nombre.delete(0, tk.END)
    entrada_precio.delete(0, tk.END)
    combo_categoria.set("")
    tabla_productos.selection_remove(tabla_productos.selection())


def obtener_producto_seleccionado():
    seleccion = tabla_productos.selection()
    if not seleccion:
        messagebox.showwarning(
            "Selección requerida",
            "Seleccione un producto de la tabla del menú."
        )
        return None
    return int(seleccion[0])


def agregar_producto():
    nombre = entrada_nombre.get().strip()
    precio_texto = entrada_precio.get().strip()
    categoria = combo_categoria.get().strip()

    if not nombre or not precio_texto or not categoria:
        messagebox.showwarning("Datos incompletos", "Complete todos los campos.")
        return

    try:
        precio = float(precio_texto)
        if precio <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning(
            "Precio inválido", "Ingrese un precio numérico mayor que cero."
        )
        return

    if any(p["nombre"].casefold() == nombre.casefold()
           for p in estructuras.productos):
        messagebox.showwarning(
            "Producto duplicado", "Ya existe un producto con ese nombre."
        )
        return

    estructuras.productos.append({
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria
    })
    actualizar_tabla_productos()
    limpiar_campos_producto()
    messagebox.showinfo("Listo", "Producto agregado al menú.")


def buscar_producto():
    nombre = entrada_nombre.get().strip().casefold()
    if not nombre:
        messagebox.showwarning(
            "Dato requerido", "Escriba el nombre del producto para buscarlo."
        )
        return

    for indice, producto in enumerate(estructuras.productos):
        if nombre in producto["nombre"].casefold():
            tabla_productos.selection_set(str(indice))
            tabla_productos.focus(str(indice))
            tabla_productos.see(str(indice))
            cargar_producto_en_campos(indice)
            return

    messagebox.showinfo("Resultado", "No se encontró el producto.")


def cargar_producto_en_campos(indice):
    producto = estructuras.productos[indice]
    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(0, producto["nombre"])
    entrada_precio.delete(0, tk.END)
    entrada_precio.insert(0, str(producto["precio"]))
    combo_categoria.set(producto["categoria"])


def seleccionar_producto(evento=None):
    seleccion = tabla_productos.selection()
    if not seleccion:
        return
    cargar_producto_en_campos(int(seleccion[0]))


def modificar_producto():
    indice = obtener_producto_seleccionado()
    if indice is None:
        return

    nombre = entrada_nombre.get().strip()
    precio_texto = entrada_precio.get().strip()
    categoria = combo_categoria.get().strip()

    if not nombre or not precio_texto or not categoria:
        messagebox.showwarning("Datos incompletos", "Complete todos los campos.")
        return

    try:
        precio = float(precio_texto)
        if precio <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning(
            "Precio inválido", "Ingrese un precio numérico mayor que cero."
        )
        return

    for otro_indice, producto in enumerate(estructuras.productos):
        if (otro_indice != indice and
                producto["nombre"].casefold() == nombre.casefold()):
            messagebox.showwarning(
                "Producto duplicado", "Otro producto ya usa ese nombre."
            )
            return

    estructuras.productos[indice] = {
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria
    }
    actualizar_tabla_productos()
    limpiar_campos_producto()
    messagebox.showinfo("Listo", "Producto modificado correctamente.")


def eliminar_producto():
    indice = obtener_producto_seleccionado()
    if indice is None:
        return

    nombre = estructuras.productos[indice]["nombre"]
    confirmar = messagebox.askyesno(
        "Confirmar eliminación",
        f"¿Desea eliminar '{nombre}' del menú?"
    )
    if not confirmar:
        return

    del estructuras.productos[indice]
    actualizar_tabla_productos()
    limpiar_campos_producto()
    messagebox.showinfo("Listo", "Producto eliminado del menú.")


def ordenar_productos():
    if not estructuras.productos:
        messagebox.showinfo("Menú vacío", "No hay productos para ordenar.")
        return
    estructuras.productos.sort(key=lambda p: p["nombre"].casefold())
    actualizar_tabla_productos()
    messagebox.showinfo("Listo", "Menú ordenado por nombre.")


# -------------------- FUNCIONES DE PEDIDOS --------------------

numero_pedido_siguiente = 1


def crear_pedido():
    global numero_pedido_siguiente

    seleccion = tabla_productos.selection()
    if not seleccion:
        messagebox.showwarning(
            "Selección requerida", "Seleccione un producto del menú."
        )
        return

    cantidad_texto = entrada_cantidad.get().strip()
    try:
        cantidad = int(cantidad_texto)
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning(
            "Cantidad inválida",
            "Ingrese una cantidad entera mayor que cero."
        )
        return

    indice = int(seleccion[0])
    producto = estructuras.productos[indice]

    pedido = {
        "numero": numero_pedido_siguiente,
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio_unitario": producto["precio"],
        "total": producto["precio"] * cantidad
    }

    estructuras.pedidos_activos.agregar(pedido)
    numero_pedido_siguiente += 1
    actualizar_tabla_pedidos()
    entrada_cantidad.delete(0, tk.END)

    messagebox.showinfo(
        "Pedido creado",
        f'Pedido N.º {pedido["numero"]} registrado.\n'
        f'Total: ₡{pedido["total"]:,.2f}'
    )


def actualizar_tabla_pedidos():
    for fila in tabla_pedidos.get_children():
        tabla_pedidos.delete(fila)

    for pedido in estructuras.pedidos_activos.mostrar():
        tabla_pedidos.insert(
            "", "end", iid=str(pedido["numero"]),
            values=(
                pedido["numero"],
                pedido["producto"],
                pedido["cantidad"],
                f'₡{pedido["precio_unitario"]:,.2f}',
                f'₡{pedido["total"]:,.2f}'
            )
        )


def buscar_pedido():
    numero_texto = entrada_numero_pedido.get().strip()
    if not numero_texto.isdigit() or int(numero_texto) <= 0:
        messagebox.showwarning(
            "Número inválido", "Ingrese un número de pedido válido."
        )
        return

    numero = int(numero_texto)
    pedido = estructuras.pedidos_activos.buscar(numero)
    if pedido is None:
        messagebox.showinfo(
            "Resultado", "No se encontró ese pedido entre los pedidos activos."
        )
        return

    clave = str(numero)
    tabla_pedidos.selection_set(clave)
    tabla_pedidos.focus(clave)
    tabla_pedidos.see(clave)


def retirar_pedido():
    seleccion = tabla_pedidos.selection()
    if not seleccion:
        numero_texto = entrada_numero_pedido.get().strip()
        if numero_texto.isdigit():
            pedido = estructuras.pedidos_activos.buscar(int(numero_texto))
            if pedido is not None:
                seleccion = (numero_texto,)

    if not seleccion:
        messagebox.showwarning(
            "Selección requerida", "Seleccione un pedido activo para retirarlo."
        )
        return

    numero = int(seleccion[0])
    confirmar = messagebox.askyesno(
        "Confirmar", f"¿Marcar el pedido N.º {numero} como atendido y retirarlo?"
    )
    if not confirmar:
        return

    if estructuras.pedidos_activos.eliminar(numero):
        actualizar_tabla_pedidos()
        entrada_numero_pedido.delete(0, tk.END)
        messagebox.showinfo(
            "Pedido atendido", f"El pedido N.º {numero} fue retirado de la lista."
        )
    else:
        messagebox.showinfo("Resultado", "El pedido ya no está activo.")


# -------------------- INTERFAZ GRAFICA --------------------

ventana = tk.Tk()
ventana.title("Sistema de Pedidos de Restaurante")
ventana.geometry("980x850")
ventana.minsize(900, 760)

titulo = tk.Label(
    ventana,
    text="SISTEMA DE PEDIDOS DE RESTAURANTE",
    font=("Arial", 17, "bold")
)
titulo.pack(pady=(12, 8))

tk.Label(
    ventana,
    text="MENÚ DE PRODUCTOS",
    font=("Arial", 12, "bold")
).pack(pady=(4, 2))

marco_campos = tk.Frame(ventana)
marco_campos.pack(pady=3)

tk.Label(marco_campos, text="Nombre:").grid(
    row=0, column=0, padx=5, pady=5, sticky="e"
)
entrada_nombre = tk.Entry(marco_campos, width=22)
entrada_nombre.grid(row=0, column=1, padx=5, pady=5)

tk.Label(marco_campos, text="Precio (₡):").grid(
    row=0, column=2, padx=5, pady=5, sticky="e"
)
entrada_precio = tk.Entry(marco_campos, width=14)
entrada_precio.grid(row=0, column=3, padx=5, pady=5)

tk.Label(marco_campos, text="Categoría:").grid(
    row=1, column=0, padx=5, pady=5, sticky="e"
)
combo_categoria = ttk.Combobox(
    marco_campos,
    values=["Comidas", "Bebidas", "Postres"],
    state="readonly",
    width=19
)
combo_categoria.grid(row=1, column=1, padx=5, pady=5, sticky="w")

marco_botones_menu = tk.Frame(ventana)
marco_botones_menu.pack(pady=4)

tk.Button(
    marco_botones_menu, text="Agregar",
    command=agregar_producto, width=12
).grid(row=0, column=0, padx=3, pady=3)
tk.Button(
    marco_botones_menu, text="Buscar",
    command=buscar_producto, width=12
).grid(row=0, column=1, padx=3, pady=3)
tk.Button(
    marco_botones_menu, text="Modificar",
    command=modificar_producto, width=12
).grid(row=0, column=2, padx=3, pady=3)
tk.Button(
    marco_botones_menu, text="Eliminar",
    command=eliminar_producto, width=12
).grid(row=0, column=3, padx=3, pady=3)
tk.Button(
    marco_botones_menu, text="Ordenar por nombre",
    command=ordenar_productos, width=18
).grid(row=0, column=4, padx=3, pady=3)
tk.Button(
    marco_botones_menu, text="Limpiar campos",
    command=limpiar_campos_producto, width=13
).grid(row=0, column=5, padx=3, pady=3)

columnas_productos = ("nombre", "precio", "categoria")
tabla_productos = ttk.Treeview(
    ventana, columns=columnas_productos, show="headings", height=6
)
tabla_productos.heading("nombre", text="Producto")
tabla_productos.heading("precio", text="Precio")
tabla_productos.heading("categoria", text="Categoría")
tabla_productos.column("nombre", width=300)
tabla_productos.column("precio", width=170, anchor="center")
tabla_productos.column("categoria", width=250, anchor="center")
tabla_productos.pack(pady=5)
tabla_productos.bind("<<TreeviewSelect>>", seleccionar_producto)

texto_categorias = tk.Label(
    ventana, text="", font=("Arial", 10, "bold")
)
texto_categorias.pack(pady=(2, 8))

tk.Label(
    ventana, text="PEDIDOS ACTIVOS", font=("Arial", 12, "bold")
).pack(pady=(3, 2))

marco_pedidos = tk.Frame(ventana)
marco_pedidos.pack(pady=3)

tk.Label(marco_pedidos, text="Cantidad:").grid(
    row=0, column=0, padx=4, pady=4
)
entrada_cantidad = tk.Entry(marco_pedidos, width=8)
entrada_cantidad.grid(row=0, column=1, padx=4, pady=4)

tk.Button(
    marco_pedidos, text="Crear pedido",
    command=crear_pedido, width=14
).grid(row=0, column=2, padx=4, pady=4)

tk.Label(marco_pedidos, text="N.º pedido:").grid(
    row=0, column=3, padx=4, pady=4
)
entrada_numero_pedido = tk.Entry(marco_pedidos, width=8)
entrada_numero_pedido.grid(row=0, column=4, padx=4, pady=4)

tk.Button(
    marco_pedidos, text="Buscar pedido",
    command=buscar_pedido, width=14
).grid(row=0, column=5, padx=4, pady=4)

columnas_pedidos = (
    "numero", "producto", "cantidad", "precio", "total"
)
tabla_pedidos = ttk.Treeview(
    ventana, columns=columnas_pedidos, show="headings", height=7
)
tabla_pedidos.heading("numero", text="N.º")
tabla_pedidos.heading("producto", text="Producto")
tabla_pedidos.heading("cantidad", text="Cantidad")
tabla_pedidos.heading("precio", text="Precio unitario")
tabla_pedidos.heading("total", text="Total")
tabla_pedidos.column("numero", width=55, anchor="center")
tabla_pedidos.column("producto", width=260)
tabla_pedidos.column("cantidad", width=90, anchor="center")
tabla_pedidos.column("precio", width=145, anchor="center")
tabla_pedidos.column("total", width=145, anchor="center")
tabla_pedidos.pack(pady=5)

tk.Button(
    ventana, text="Retirar pedido atendido",
    command=retirar_pedido, width=25
).pack(pady=6)

actualizar_tabla_productos()
actualizar_tabla_pedidos()
ventana.mainloop()
