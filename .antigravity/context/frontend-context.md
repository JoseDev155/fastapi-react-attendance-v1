# Contexto del frontend
## Arquitectura del frontend

```
frontend/
├───public/
│   ├── api/             # Servicios para conectar con FastAPI (fetch/axios)
│   ├── assets/          # Imágenes, logos institucionales, fuentes
│   ├── components/      # UI Atómica: Botones, Tablas, Modales de carga
│   ├── context/         # Estado Global (Auth, Notificaciones)
│   ├── hooks/           # Lógica de estado (useAuth, useAttendance)
│   ├── layouts/         # Envoltorios de página (MainLayout, AuthLayout)
│   ├── lib/             # Configuración de librerías externas
│   ├── pages/           # Vistas completas (LoginPage, DashboardPage)
│   ├── utils/           # Validadores de archivos y formateadores de fecha
│   ├── App.jsx          # Configuración de Rutas
│   ├───index.css
│   └───main.jsx
├───index.html
├───README-frontend.md
└───(otros archivos del frontend)
```