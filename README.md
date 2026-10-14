# Sistema de Pedidos de Restaurante

**Estudiante:** Anthony Jiménez  
**Curso:** Organización de Archivos y Estructura de Datos (ISB-08)  
**Proyecto elegido:** Opción 4 — Pedidos de restaurante  
**Lenguaje:** Python 3.13  
**Interfaz gráfica:** Tkinter

## Descripción

Aplicación de escritorio para administrar el menú de un restaurante y registrar pedidos. Permite agregar, buscar, modificar, eliminar y ordenar productos; crear pedidos con cantidades; calcular sus totales; consultar pedidos activos y retirar los pedidos atendidos.

## Requisitos

- Python 3.13 o una versión compatible con Tkinter.
- Visual Studio Code (opcional, para editar el código).

Tkinter normalmente viene incluido en Python para Windows. No se requieren paquetes externos.

## Cómo ejecutar

1. Descargue o clone este repositorio.
2. Abra la carpeta `SistemaPedidosRestaurante` en Visual Studio Code.
3. Abra la terminal desde **Terminal → Nueva terminal**.
4. Ejecute:

   ```bash
   python main.py
   ```

   Si en su equipo el comando `python` no funciona, pruebe:

   ```bash
   py main.py
   ```

## Archivos del proyecto

- `main.py`: interfaz gráfica y funciones para administrar productos y pedidos.
- `estructuras.py`: definición y operaciones de las estructuras de datos.
- `README.md`: información e instrucciones del proyecto.

## Estructuras de datos utilizadas

| Estructura | Uso en la aplicación | Ubicación |
|---|---|---|
| Vector o arreglo | `cantidades` guarda el número de productos de cada categoría. Se inicializa, accede por índice y se recorre para actualizar los conteos. | `estructuras.py`, función `actualizar_cantidades()` |
| Lista dinámica (equivalente a ArrayList) | `productos` guarda el catálogo. La aplicación agrega, consulta, modifica, elimina y ordena productos. | `estructuras.py`, variable `productos`; operaciones en `main.py` |
| Lista enlazada simple propia | Cada `Nodo` contiene un pedido y una referencia `siguiente`. Permite agregar, buscar, recorrer y eliminar pedidos activos. | `estructuras.py`, clases `Nodo` y `ListaEnlazada`; uso en `main.py` |

## Datos de prueba

Al iniciar, el menú contiene estos productos de ejemplo:

- Hamburguesa — ₡2.500 — Comidas
- Pizza — ₡3.500 — Comidas
- Refresco — ₡1.000 — Bebidas
- Helado — ₡1.200 — Postres

Para probar pedidos, seleccione un producto en el menú, escriba una cantidad entera positiva y pulse **Crear pedido**. Para buscar un pedido, escriba su número en el campo correspondiente. Para retirarlo, selecciónelo en la tabla y pulse **Retirar pedido atendido**.

Ejemplo: dos hamburguesas a ₡2.500 cada una deben generar un total de ₡5.000.


