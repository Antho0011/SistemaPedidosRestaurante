# Estructuras de datos del Sistema de Pedidos de Restaurante

# Lista dinámica (equivalente a ArrayList): catálogo de productos.
productos = [
    {"nombre": "Hamburguesa", "precio": 2500.0, "categoria": "Comidas"},
    {"nombre": "Pizza", "precio": 3500.0, "categoria": "Comidas"},
    {"nombre": "Refresco", "precio": 1000.0, "categoria": "Bebidas"},
    {"nombre": "Helado", "precio": 1200.0, "categoria": "Postres"}
]

# Vector: una posición por categoría, con su cantidad de productos.
categorias = ["Comidas", "Bebidas", "Postres"]
cantidades = [0, 0, 0]


def actualizar_cantidades():
    """Cuenta cuántos productos hay en cada categoría."""
    for indice in range(len(cantidades)):
        cantidades[indice] = 0

    for producto in productos:
        for indice in range(len(categorias)):
            if producto["categoria"] == categorias[indice]:
                cantidades[indice] += 1


# Nodo de la lista enlazada: contiene un pedido y el enlace al siguiente nodo.
class Nodo:
    def __init__(self, pedido):
        self.pedido = pedido
        self.siguiente = None


# Lista enlazada simple para mantener los pedidos activos.
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, pedido):
        nuevo = Nodo(pedido)

        if self.cabeza is None:
            self.cabeza = nuevo
            return

        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def mostrar(self):
        pedidos = []
        actual = self.cabeza

        while actual is not None:
            pedidos.append(actual.pedido)
            actual = actual.siguiente

        return pedidos

    def buscar(self, numero):
        actual = self.cabeza

        while actual is not None:
            if actual.pedido["numero"] == numero:
                return actual.pedido
            actual = actual.siguiente

        return None

    def eliminar(self, numero):
        actual = self.cabeza
        anterior = None

        while actual is not None:
            if actual.pedido["numero"] == numero:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True

            anterior = actual
            actual = actual.siguiente

        return False


# Una instancia compartida por la interfaz.
pedidos_activos = ListaEnlazada()

# Inicializamos el vector con el catálogo de ejemplo.
actualizar_cantidades()
