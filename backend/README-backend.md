# Backend

# Índice

- [Backend](#backend)
- [Índice](#índice)
  - [Arquitectura del Backend](#arquitectura-del-backend)
  - [Tecnologías del Backend](#tecnologías-del-backend)
  - [Instrucciones para el Backend](#instrucciones-para-el-backend)
    - [Desarrollo](#desarrollo)
      - [**Para Anaconda**](#para-anaconda)
      - [**Para Python**](#para-python)
  - [Librerías de Python para el análisis de datos](#librerías-de-python-para-el-análisis-de-datos)

## Arquitectura del Backend

Es un **MVC (Modelo-Vista-Controlador) extendido**:

```plaintext
backend/
├───database/       # Configuración de la base de datos y conexión
│   └───scripts/
│       └───test/
├───exports/        # Archivos exportados, como reportes o datos de asistencias
├───logs/           # Archivos de logs para monitoreo y depuración
├───metrics/        # Métricas de asistencias, puntualidad, etc.
├───models/         # Modelos (M)
├───reports/        # Reportes generados a partir de los datos de asistencias
├───repositories/   # Repositorios para acceso a datos
├───routers/        # Controladores, rutas o endpoints de la API (V, C)
├───schemas/        # Esquemas para validación y serialización de datos
├───services/       # Servicios, para la lógica de negocio
├───sockets/        # WebSockets para comunicación en tiempo real (si se implementa)
├───uploads/        # Archivos subidos por los usuarios, como Excels de asistencias
├───utils/          # Funciones de utilidad, como seguridad, autenticación, etc.
└───main.py         # Punto de entrada de la aplicación (Ruta principal)
```

EL MVC tradicional se compone de:

* **Modelos:** Representan las entidades de la base de datos (tablas) y se definen usando **SQLAlchemy**.
* **Vistas:** En FastAPI, las vistas se implementan como rutas o endpoints que manejan las solicitudes HTTP y devuelven respuestas.
* **Controladores:** Las rutas de la API.

Extensión del MVC:

* **Repositorios:** Encapsulan la lógica de acceso a datos, osea, las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) que se pueden hacer en la Base de Datos.
* **Servicios:** Lógica de negocio. Aquí se ejecutan los métodos de los repositorios y se aplican algunas validaciones.
* **Esquemas (Schemas):** Definen la estructura de los datos que se reciben y se envían a través de la API, usando **Pydantic** para validación y serialización.
* **Utilidades:** Funciones que se pueden usar para inyectar dependencias en las rutas, como la conexión a la base de datos, la seguridad o la autenticación de usuarios. Están en la carpeta `utils/`.
* **Otros módulos**

## Tecnologías del Backend

* **Motor de Base de Datos:** [PostgreSQL](https://www.postgresql.org/)
* **Sistema de Gestión de Base de Datos (SGBD, osea, UI):** [pgAdmin](https://www.pgadmin.org/)
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Versión de Python:** [Python](https://www.python.org/) `3.14.3`
* **Entorno de Desarrollo para Python:** [Anaconda](https://www.anaconda.com/) (opcional)

## Instrucciones para el Backend

### Desarrollo

> **Renombrar el archivo `base.env` a `.env`.**

#### **Para Anaconda**

1. Crear un entorno virtual con Anaconda

```bash
cd backend
conda create -n asistencias python=3.14.3
```

* `python=3`: Especifica que se va a usar la última versión de **Python 3** disponible en Anaconda

2. Activar el entorno virtual

```bash
conda activate asistencias
```

3. Instalar las dependencias

```bash
pip install -r requirements.txt
pip install -r requirements-conda.txt
```

* `requirements.txt`: Contiene las dependencias principales del proyecto
* `requirements-conda.txt`: Contiene las dependencias exactas usadas con la versión específica de Python usadas con Anaconda

4. Configurar la base de datos PostgreSQL y actualizar las variables de entorno en el archivo `.env` con las credenciales correspondientes.

6. Ejecutar el servidor de desarrollo

```bash
uvicorn main:app --reload
```

* `--reload`: Permite que el servidor se reinicie automáticamente cada vez que se realicen cambios en el código

#### **Para Python**

1. Crear un entorno virtual

```bash
cd backend
python -m venv asistencias
```

2. Activar el entorno virtual

* **En Windows:**

```bash
asistencias\Scripts\activate
```

* **En macOS/Linux:**

```bash
source asistencias/bin/activate
```

3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

4. Configurar la base de datos PostgreSQL y actualizar las variables de entorno en el archivo `.env` con las credenciales correspondientes.

6. Ejecutar el servidor de desarrollo

```bash
uvicorn main:app --reload
```


> **FastAPI** genera una documentacioón automática de la API que se puede acceder a través de:


```plaintext
http://localhost:8000/docs
```

## Librerías de Python para el análisis de datos

* `pandas`: para la manipulación y análisis de datos, especialmente útil para manejar los datos de asistencias y generar reportes.
* `numpy`: para operaciones numéricas y manejo de arrays, que pueden ser útiles para cálculos relacionados con la puntualidad y los retardos.
* `openpyxl`: para leer y escribir archivos Excel, lo que facilita la importación de datos de asistencias desde archivos `.xlsx` y la generación de reportes en formato Excel.
