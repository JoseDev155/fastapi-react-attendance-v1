# Librerias
import re
from datetime import date, time
from io import BytesIO
from sqlalchemy.orm import Session
import openpyxl
# Importar directorios del proyecto
from repositories import (
    attendance_search_by_enrollment_and_date as search_by_enrollment_and_date,
    attendance_create as create,
    attendance_update as update)


def get_month_number(nombre_mes: str) -> int:
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    return meses.get(nombre_mes.lower().strip(), 1)


def parse_arrival_time(cell_value) -> time | None:
    """
    Convierte el valor de una celda del Excel a un objeto time.
    Acepta:
      - Objetos time/datetime de openpyxl (cuando la celda tiene formato hora)
      - Strings con formatos: "HH:MM", "HH:MM:SS", "H:MM AM/PM"
      - None / cadena vacía → devuelve None (estudiante AUSENTE)
    """
    if cell_value is None:
        return None

    # openpyxl puede devolver directamente un datetime o time
    if isinstance(cell_value, time):
        return cell_value

    # openpyxl a veces retorna datetime para celdas con formato hora
    from datetime import datetime as dt
    if isinstance(cell_value, dt):
        return cell_value.time()

    raw = str(cell_value).strip()
    if not raw:
        return None

    # Intentar parsear "HH:MM" o "HH:MM:SS"
    for fmt in ("%H:%M:%S", "%H:%M", "%I:%M %p", "%I:%M:%S %p"):
        try:
            return dt.strptime(raw, fmt).time()
        except ValueError:
            continue

    return None  # Valor no reconocido → se trata como ausente


def process_attendance_excel(file_content: bytes, db: Session) -> dict:
    wb = openpyxl.load_workbook(BytesIO(file_content), data_only=True)
    ws = wb.active

    # ─── Extraer mes y año del encabezado ────────────────────────────────────
    # La plantilla generada escribe "Registro de Asistencias (Mes AAAA)" en E1
    header_title = ws["E1"].value
    if not header_title:
        raise ValueError(
            "Encabezado de mes/año no encontrado en E1. "
            "Confirme que la plantilla tiene el formato correcto."
        )

    match = re.search(r'\((.*?)\s+(\d{4})\)', str(header_title))
    if not match:
        raise ValueError(f"No se pudo extraer el mes y año del texto: {header_title}")

    mes_str, year_str = match.groups()
    month = get_month_number(mes_str)
    year  = int(year_str)

    # ─── Identificar columnas de días (Fila 2, a partir de columna E) ────────
    # Estructura de la plantilla:
    #   Col A: ENROLLMENT_ID (oculto)
    #   Col B: APODO
    #   Col C: NOMBRE COMPLETO
    #   Col D: HORA ENTRADA (referencia, no se usa para el import)
    #   Col E…N: días del mes con cabecera "Lun 06", "Mar 07", etc.
    #   Col N+1: NOTAS / OBSERVACIONES
    day_columns: dict[int, int] = {}  # col_index → número de día del mes
    max_col = ws.max_column

    for c in range(5, max_col + 1):
        cell_val = ws.cell(row=2, column=c).value
        if cell_val is None:
            continue
        cell_str = str(cell_val).strip()
        if cell_str.upper().startswith("NOTAS"):
            break  # Terminamos de leer días

        d_match = re.search(r'(\d+)', cell_str)
        if d_match:
            day_columns[c] = int(d_match.group(1))

    total_insertados  = 0
    total_actualizados = 0
    total_omitidos    = 0

    # ─── Procesar filas de estudiantes (desde la 3) ───────────────────────────
    for r in range(3, ws.max_row + 1):
        enrollment_id_raw = ws.cell(row=r, column=1).value
        if not enrollment_id_raw:
            break  # Fin de la tabla

        try:
            enrollment_id = int(enrollment_id_raw)
        except (ValueError, TypeError):
            total_omitidos += 1
            continue

        for col_index, day in day_columns.items():
            cell = ws.cell(row=r, column=col_index)

            # Cada celda contiene la HORA DE LLEGADA (o None si estaba ausente)
            arrival = parse_arrival_time(cell.value)

            # Extraer nota si existe
            notes: str | None = None
            if cell.comment:
                notes = cell.comment.text

            attendance_date = date(year, month, day)

            # Buscar registro existente
            existing = search_by_enrollment_and_date(db, enrollment_id, attendance_date)

            if existing:
                # Solo actualizar si cambió algo relevante
                changed = (existing.arrival_time != arrival) or (existing.notes != notes)
                if changed:
                    update(db, existing.id,
                           attendance_date=attendance_date,
                           arrival_time=arrival,
                           notes=notes)
                    total_actualizados += 1
                else:
                    total_omitidos += 1
            else:
                # Solo crear registro si hay algún dato (hora o nota)
                if arrival is not None or notes is not None:
                    create(db,
                           attendance_date=attendance_date,
                           arrival_time=arrival,
                           notes=notes,
                           enrollment_id=enrollment_id)
                    total_insertados += 1
                # Si la celda está vacía (sin hora y sin nota) se omite silenciosamente

    return {
        "success": True,
        "inserted": total_insertados,
        "updated":  total_actualizados,
        "skipped":  total_omitidos,
        "received_month": month,
        "received_year":  year,
        "logs": []
    }
