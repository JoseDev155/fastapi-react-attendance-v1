---
description: Ejecutar comandos en el entorno <entorno> de Anaconda
---
Para ejecutar cualquier comando de Python o script en el entorno correcto, usa la ruta absoluta de `conda.exe`:

```powershell
& "C:\Users\<Mi-Usuario>\anaconda3\Scripts\conda.exe" run -n ubbj-v1 python <tu_comando>
```

Se te dara el nombre del entorno de Anaconda y luego vas a chechear mi nombre de usuario en Windows.

Esto garantiza que se utilicen las librerías instaladas en `ubbj-v1` (FastAPI, SQLAlchemy, openpyxl, etc.) en lugar del Python global.
