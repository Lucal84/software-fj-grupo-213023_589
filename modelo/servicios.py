from abc import abstractmethod

try:
    from modelo.entidad import Entidad
except ImportError:
    from entidad import Entidad 

class Servicio(Entidad):
    """clase abstracta para los servicios que se ofrecen"""
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, disponible: bool= True):
        super().__init__(identificador) #inicializa el identificador heredado de entidad
        self.nombre = nombre 
        self.tarifa_base = tarifa_base #la tarifa es lo que cuesta el servicio por una hora, mas adelante se utiliza "duracion" para cuantas horas se reservará el servicio
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) : #valida que el nombre tenga al menos 3 caracteres
        if not valor or len(valor.strip()) <3 :
            raise ValueError("el nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float): #valida que la tarifa sea positiva
        if valor is None or valor <=0:
            raise ValueError("la tarifa base debe ser mayor a cero")
        self._tarifa_base = float(valor)

    def aplicar_ajustes(self, subtotal: float, impuesto: float = 0.0, descuento: float = 0.0) -> float :
        """permite aplicar impuestos y descuentos al precio final del servicio"""
         # el subtotal es la tarifa base ya operada con la duracion y las reglas propias de cada servicio
        #el metodo toma el subtotal, le resta el descuento y le suma el impuesto (éste último calculado sobre el valor total ya afectado por el descuento)
        #los impuestos y descuentos son porcentajes directos (4.01 -> 4.01%)
        if impuesto < 0 or descuento < 0:
            raise ValueError("el impuesto y el descuento no puede ser negativos")
        if descuento > 100:
            raise ValueError("el descuento no puede ser mayor al 100%")
        valor_descuento = subtotal*(descuento/100)
        total = subtotal - valor_descuento
        valor_impuesto = total*(impuesto/100)
        total +=valor_impuesto
        return round(total, 2)

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool): #valida que la disponibilidad sea booleano
        if not isinstance(valor, bool):
            raise ValueError("la disponibilidad debe ser True o False")
        self._disponible = valor

    def validar_parametros(self, duracion: int):
        """verifica que el servicio esté disponible y que la duración sea valida"""

        if not self.disponible:
            raise ValueError(f'el servicio "{self.nombre}" no está disponible en este momento')
        if not isinstance(duracion, int) or duracion <= 0:
            raise ValueError("la duracion debe ser un numero entero mayor a 0")

    @abstractmethod
    def calcular_costo(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) ->float :
        """calcula el costo total según el tipo de servicio y parámetros opcionales"""
        pass


class ReservaSala(Servicio):
    """servicio especializado para reserva de salas"""
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, capacidad: int, disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("la capacidad de la sala debe ser mayor a 0")
        self._capacidad = valor
 
    def calcular_costo(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        self.validar_parametros(duracion) #valida la disponibilidad y la duración antes de hacer los cálculos
        subtotal = self.tarifa_base * duracion
        if self.capacidad > 20 : #añade un aumento dell 20% en el subtotal si la sala es muy grande
            subtotal += subtotal * 0.20
        return self.aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        estado ="disponible" if self.disponible else "no disponible"
        return f"sala [ID: {self.identificador} - {self.nombre} - capacidad: {self.capacidad} personas - tarifa por hora: ${self.tarifa_base} - {estado}]"


class AlquilerEquipo(Servicio):
    """servicio especializado para alquiler de equipos tecnológicos"""
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, cantidad_equipos: int, disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.cantidad_equipos = cantidad_equipos

    @property
    def cantidad_equipos(self) ->int:
        return self._cantidad_equipos

    @cantidad_equipos.setter
    def cantidad_equipos(self, valor: int):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("la cantidad de equipos debe ser almenos 1")
        self._cantidad_equipos = valor

    def calcular_costo(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        self.validar_parametros(duracion) #el costo depende de la tarifa, las horas y la cantidad de equipos
        subtotal = self.tarifa_base * duracion * self.cantidad_equipos
        return self.aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return f"equipo [ID: {self.identificador} - {self.nombre} - cantidad: {self.cantidad_equipos} - tarifa: ${self.tarifa_base} - {estado}]"


class Asesoria(Servicio):
    """servicio para asesorias"""
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True):
        super().__init__(identificador, nombre, tarifa_base, disponible)
        self.especialidad = especialidad

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ValueError("la especialidad debe tener al menos 3 caracteres")
        self._especialidad = valor.strip()

    def calcular_costo(self, duracion: int, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        self.validar_parametros(duracion)
        subtotal = self.tarifa_base * duracion
        return self.aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return f"asesoría [ID:  {self.identificador} - {self.nombre} ({self.especialidad}) - tarifa/h: ${self.tarifa_base} - {estado}]"


