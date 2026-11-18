try: # para que la importación sea compatible así se ejecute desde main.py o desde modelo/
    from modelo.entidad import Entidad
except ImportError:
    from entidad import Entidad

class Cliente(Entidad):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre= nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3 :
            raise ValueError("el nombre debe tener al menos 3 caracteres")
        self._nombre = valor.strip()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not valor.isdigit() or len(valor) < 7 :
            raise ValueError("el numero de telefono debe contener solo numeros y almenos 7 dígitos")
        self._telefono = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not valor or "@" not in valor or "." not in valor:
            raise ValueError("el formato del correo elctronico no es valido")
        self._correo = valor.strip()

    def describir(self)-> str:
        return f"cliente [ID: {self.identificador} - nombre: {self.nombre} - correo: {self.correo} - teléfono: {self.telefono} ]"
    