# Lógica del backend

* Para archivos de Python, usa snake_case.
* Para clases, funciones y variables, ya tienes instrucciones en el `AGENT.md`.
* La API y los endpoints base ya están terminados.
* Implementa los módulos que tienen un asterisco (*) en el `backend-context.md`.
* No modifiques los módulos que no tienen un asterisco (*) salvo que sea necesario y pidas permiso.
* Para la extracción de comentarios de celdas en archivos `.xlsx`, utiliza `openpyxl`. `pandas` por sí solo no tiene acceso a los objetos de comentario de Excel.

# Lógica del frontend

* Para archivos de JavaScript y Hooks, usa camelCase.
* En el caso de componentes y páginas, usa PascalCase.
* Estructura de nombres:
  * `components/`: `Button.jsx`, `Table.jsx` (Piezas atómicas)
  * `pages/`: `HomePage.jsx`, `LoginPage.jsx` (Vistas completas)
  * `layouts/`: `MainLayout.jsx` (Contenedores que envuelven rutas)
* Usa `fetch()` nativo. Implementa una función de utilidad global para manejar `response.ok` y catch de errores.

# Lógica por implementar: Cargar asistencias

* Frontend: El usuario arrastra el Excel al componente de carga.
* Frontend: Se valida que sea .xlsx y se envía mediante un POST al endpoint de FastAPI.
* Backend: FastAPI recibe el archivo, lo abre con pandas y realiza un UPSERT (Update or Insert) en PostgreSQL.
* Lógica del Delta: El backend compara por ID_Estudiante y Fecha. Si el registro existe, lo ignora o lo actualiza; si no existe, lo crea.
* Backend: Responde con un resumen: "Se cargaron 50 registros, 5 eran duplicados e ignorados".
* Frontend: Muestra una alerta elegante con el resultado.

# Tipografía

* Uso obligatorio de 'Instrument Sans' para título e 'Inter' para datos/tablas.

# Prioridades

* Trabaja pensando en reutilizar componentes y estilos.
* Crea componentes para las tarjetas o cualquier elemento que se repita.
* Maneja carpetas y subcarpetas acorde a las páginas que estás trabajando.
* No hagas configuraciones de librerías sin consultar primero.
