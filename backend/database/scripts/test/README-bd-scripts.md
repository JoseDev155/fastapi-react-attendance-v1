# Test Scripts - Archivos de Prueba

Este directorio contiene plantillas de prueba para operaciones CRUD en la base de datos.

## Forma de ejecutarlos

Estando logueados a la BD, ejecutamos en la terminal o gestor visual de SQL (**pgAdmin** es el maás famoso en el caso de PostreSQL) el siguiente comando:

```bash
psql -U postgres -d asistencias_ubbj -f <archivo1>.sql
psql -U postgres -d asistencias_ubbj -f <archivo2>.sql
```

Luego, descomentar los comandos SQL que se quieran probar, y ejecutarlos para verificar su funcionamiento.