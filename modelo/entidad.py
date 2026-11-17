from abc import ABC, abstractmethod

class Entidad(ABC):
    """clase abstracta que representa entidades generales del sistema"""
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self)-> str:
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """método abstracto obligatorio para describir la entidad."""
        pass

