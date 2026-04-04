# Contexto del backend
## Arquitectura del backend

>`openapi.json`

```
backend/
├───database/       # Configuración de la base de datos y conexión
│   └───scripts/
│       └───test/
├───exports/        # *Archivos exportados, como reportes o datos de asistencias
├───logs/           # Archivos de logs para monitoreo y depuración
├───metrics/        # *Métricas de asistencias, puntualidad, etc.
├───models/         # Modelos (M)
├───reports/        # *Reportes generados a partir de los datos de asistencias
├───repositories/   # Repositorios para acceso a datos
├───routers/        # Controladores, rutas o endpoints de la API (V, C)
├───schemas/        # Esquemas para validación y serialización de datos
├───services/       # Servicios, para la lógica de negocio
├───sockets/        # *WebSockets para comunicación en tiempo real (si se implementa)
├───uploads/        # *Archivos subidos por los usuarios, como Excels de asistencias
├───utils/          # Funciones de utilidad, como seguridad, autenticación, etc.
└───main.py         # Punto de entrada de la aplicación
```