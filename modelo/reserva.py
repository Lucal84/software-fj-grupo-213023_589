try:
    from modelo.entidad import Entidad
    from modelo.cliente import Cliente
    from modelo.servicios import Servicio
except ImportError:
    from entidad import Entidad
    from cliente import Cliente
    from servicios import Servicio


class Reserva(Entidad):
    """gestiona la reserva de un servicio por parte de un cliente"""

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, duracion: int):
        super().__init__(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self._estado = "PENDIENTE" #los estados que se manejarán serán: "PENDIENTE", "CONFIRMADA", "CANCELADA" y "PROCESADA", Toda reserva inicia en estado "PENDIENTE"
        self._costo_total = 0.0

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @cliente.setter
    def cliente(self, valor: Cliente): # Verifica que se reciba una instancia válida de Cliente
        if not isinstance(valor, Cliente):
            raise ValueError("debe asignar un objeto Cliente válido a la reserva")
        self._cliente = valor

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @servicio.setter
    def servicio(self, valor: Servicio): #verifica que se reciba una instancia válida de Servicio
        if not isinstance(valor, Servicio):
            raise ValueError("Debe asignar un objeto Servicio válido a la reserva")
        self._servicio = valor

    @property
    def duracion(self) -> int:
        return self._duracion

    @duracion.setter
    def duracion(self, valor: int): #valida la duración usando las reglas del servicio
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("la duración de la reserva debe ser mayor a 0")
        self._servicio.validar_parametros(valor)
        self._duracion = valor

    @property
    def estado(self) ->str:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar(self, impuesto: float = 0.0, descuento: float = 0.0):
        """confirma la reserva si está pendiente y calcula su costo total"""
        if self._estado != "PENDIENTE": #si el estado es distinto a "PENDIENTE" no se puede confirmar
            raise ValueError(f"no se puede confirmar una reserva en estado '{self._estado}'")
        self._servicio.validar_parametros(self._duracion) #verifica si el servicio sigue disponible
        self._costo_total = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        self._estado = "CONFIRMADA"

    def cancelar(self):
        """cancela la reserva siempre que no haya sido procesada o cancelada antes"""
        if self._estado in ("CANCELADA", "PROCESADA"):
            raise ValueError(f"no se puede cancelar una reserva en estado '{self._estado}'")
        self._estado = "CANCELADA"

    def procesar(self):
        """finaliza y procesa la reserva una vez que ha sido confirmad"""
        if self._estado != "CONFIRMADA":
            raise ValueError("solo se pueden procesar reservas que estén en estado CONFIRMADA")
        self._estado = "PROCESADA"

    def describir(self) -> str:
        return (
            f"reserva [ID: {self.identificador} - cliente: {self.cliente.nombre} - "
            f"servicio: {self.servicio.nombre} - duración: {self.duracion}h - "
            f"estado: {self.estado} - total: ${self.costo_total}]"
        )