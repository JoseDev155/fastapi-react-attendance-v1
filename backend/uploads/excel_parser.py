# Librerias
import re
from datetime import date, datetime
from io import BytesIO
from sqlalchemy.orm import Session
import openpyxl
# Importar directorios del proyecto
from models import AttendanceStatus
from repositories import (
    attendance_search_by_enrollment_and_date as search_by_enrollment_and_date, \
    attendance_create as create, \
    attendance_update as update)

def get_month_number(nombre_mes: str) -> int:
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    return meses.get(nombre_mes.lower().strip(), 1)

def translate_status(estado_es: str) -> AttendanceStatus | None:
    if not estado_es:
        return None
        
    estado = str(estado_es).strip().upper()
    if estado == "PRESENTE":
        return AttendanceStatus.PRESENT
    elif estado == "AUSENTE":
        return AttendanceStatus.ABSENT
    elif estado == "TARDE":
        return AttendanceStatus.LATE
    elif estado == "JUSTIFICADO":
        return AttendanceStatus.JUSTIFIED
    elif estado == "SALIO TEMPRANO" or estado == "SALIO":
        return AttendanceStatus.LEFT_EARLY
    return None

def process_attendance_excel(file_content: bytes, db: Session) -> dict:
    wb = openpyxl.load_workbook(BytesIO(file_content), data_only=True)
    ws = wb.active

    # Extraer mes y año del encabezado
    # El encabezado E1 está mergeado pero la celda E1 guarda el valor
    header_title = ws["E1"].value
    if not header_title:
         raise ValueError("Encabezado de mes/año no encontrado en E1. Verifique que la columna D (o E) contiene el título del mes.")
         
    # Regex para extraer "Registro de Asistencias (Octubre 2025)"
    match = re.search(r'\((.*?)\s+(\d{4})\)', str(header_title))
    if not match:
        raise ValueError(f"No se pudo extraer el mes y año del texto: {header_title}")
        
    mes_str, year_str = match.groups()
    month = get_month_number(mes_str)
    year = int(year_str)

    # Identificar las columnas de los días leyendo la Fila 2
    day_columns = {} # col_index -> day (int)
    max_col = ws.max_column
    
    # La columna 1 es ID, 2 es Apodo, 3 es Nombre, 4 es Hora
    # Empezamos buscando desde la 5
    for c in range(5, max_col + 1):
        cell_val = ws.cell(row=2, column=c).value
        cell_str = str(cell_val).strip()
        if cell_str.lower().startswith("notas"):
            break # Terminamos de leer dias
        
        # Debe decir algo como "Lun 06" -> extraer el numero
        d_match = re.search(r'(\d+)', cell_str)
        if d_match:
            day_columns[c] = int(d_match.group(1))

    total_procesados = 0
    total_actualizados = 0
    
    # Procesar filas a partir de la 3
    for r in range(3, ws.max_row + 1):
        enrollment_id = ws.cell(row=r, column=1).value
        # Si no hay ID, terminamos las filas útiles
        if not enrollment_id:
            break
            
        try:
            enrollment_id = int(enrollment_id)
        except ValueError:
            continue
            
        for col_index, day in day_columns.items():
            cell = ws.cell(row=r, column=col_index)
            status_es = cell.value
            
            attendance_status = translate_status(status_es)
            if not attendance_status:
                continue # Celda vacía o estado no válido
                
            # Extraer comentario si existe como nota
            notes = None
            if cell.comment:
                notes = cell.comment.text
                
            attendance_date = date(year, month, day)
            
            # Buscar si ya existe la asistencia para esa fecha y enrollment
            existing = search_by_enrollment_and_date(db, enrollment_id, attendance_date)
            
            # TODO: Convertir la "HORA ENTRADA" si es LATE? Por ahora NULL ya que el cliente
            # registraría manual o el estado lo define.
            
            if existing:
                if existing.status != attendance_status or existing.notes != notes:
                    update(db, existing.id, attendance_date=attendance_date, 
                           status=attendance_status, notes=notes)
                    total_actualizados += 1
            else:
                create(db, attendance_date=attendance_date, arrival_time=None, 
                       status=attendance_status, notes=notes, enrollment_id=enrollment_id)
                total_procesados += 1
                
    return {
        "success": True,
        "nuevos_registros": total_procesados,
        "registros_actualizados": total_actualizados,
        "mes": month,
        "año": year
    }
