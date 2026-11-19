# software-fj-grupo-213023_589

**Fase 4 - Componente práctico - Prácticas simuladas**  
Curso: Programación (213023) - UNAD

## Descripción del proyecto
Aplicación desarrollada en Python bajo el paradigma de Programación Orientada a Objetos (POO) con manejo avanzado de excepciones, validaciones estrictas y registro de eventos en archivos (sin base de datos).

## Integrantes
- Esloder Alvarez (`Xloder-17`)
- Jefferson Aya (`Jeffersona_Aya`)
- Lucal84 (`Lucal84`)

## Estructura del proyecto
- `modelo/`: Clases base del sistema (`entidad.py`, `cliente.py`, `servicios.py`, `reserva.py`).
- `simulaciones.py`: Script con 12 operaciones de prueba (válidas e inválidas), manejo de excepciones (`try/except/else/finally`), excepción personalizada encadenada y registro de logs.
- `logs/eventos.log`: Registro automático de eventos y errores.
- `docs/capturas/`: Evidencias de ejecución del sistema.

## Ejecución
1. Clonar el repositorio:
   `git clone https://github.com/Lucal84/software-fj-grupo-213023_589.git`
2. Ejecutar las simulaciones desde la terminal:
   `python simulaciones.py`
3. *(Para el sistema interactivo completo, ejecutar `python main.py` una vez integrado).*

## Evidencias de ejecución

### Ejecución de simulaciones (12 operaciones)
![Simulaciones](docs/capturas/Simulaciones.png)

### Registro de eventos y errores (`logs/eventos.log`)
![Logs](docs/capturas/logs.png)