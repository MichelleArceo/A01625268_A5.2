# A5.2 - Compute Sales (Python)

Este proyecto calcula el costo total de ventas a partir de:
1) Un catálogo de productos con precio (`title`, `price`)
2) Un registro de ventas (`Product`, `Quantity`)

El programa:
- Se ejecuta por línea de comandos con 2 archivos JSON
- Imprime un reporte en consola
- Genera un archivo `SalesResults.txt` con el mismo reporte
- Continúa la ejecución ante filas inválidas (se reportan como errores/advertencias)
- Incluye el tiempo transcurrido de ejecución

Nota: Las cantidades negativas en `Quantity` se consideran en el cálculo del total (por ejemplo, devoluciones/ajustes).

---

## Requisitos
- Python 3.x
- Paquetes para análisis estático:
  - flake8
  - pylint

Instalación (local):
```bash
pip install flake8 pylint
