# Librerias
import calendar
from datetime import date
from io import BytesIO
from typing import List, Dict, Any
from sqlalchemy.orm import Session
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def generate_attendance_template(
    year: int,
    month: int,
    students_data: List[Dict[str, Any]]
) -> BytesIO:
    """
    Genera un archivo Excel (.xlsx) usado como plantilla de asistencia mensual.
    students_data debe contener diccionarios con:
      - enrollment_id: (int)
      - nickname: (str)
      - full_name: (str)
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Asistencias {year}-{month:02d}"

    # Estilos básicos
    header_fill = PatternFill(start_color="343A40", end_color="343A40", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    alignment_center = Alignment(horizontal="center", vertical="center")
    alignment_left = Alignment(horizontal="left", vertical="center")
    
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )

    # Nombres de meses en español
    meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    dias_semana = ["Lun", "Mar", "Mie", "Jue", "Vie", "Sab", "Dom"]

    _, num_days = calendar.monthrange(year, month)
    
    # --------------------
    # Definir estructura
    # --------------------
    # Fila 1: Títulos generales
    ws.merge_cells("B1:D1")
    ws["B1"] = "Datos del Estudiante"
    ws["B1"].fill = header_fill
    ws["B1"].font = header_font
    ws["B1"].alignment = alignment_center
    ws["B1"].border = thin_border

    # Días exactos y validos
    dias_validos = []
    for day in range(1, num_days + 1):
        weekday = calendar.weekday(year, month, day)
        if weekday < 5:  # Lunes a Viernes -> 0 a 4
            dias_validos.append((day, weekday))
            
    col_dias_start = 5 # Columna E
    col_dias_end = col_dias_start + len(dias_validos) - 1
    
    start_letter = get_column_letter(col_dias_start)
    end_letter = get_column_letter(col_dias_end)
    
    ws.merge_cells(f"{start_letter}1:{end_letter}1")
    ws[f"{start_letter}1"] = f"Registro de Asistencias ({meses[month]} {year})"
    ws[f"{start_letter}1"].fill = header_fill
    ws[f"{start_letter}1"].font = header_font
    ws[f"{start_letter}1"].alignment = alignment_center
    ws[f"{start_letter}1"].border = thin_border
    
    # Notas
    notes_col = col_dias_end + 1
    notes_letter = get_column_letter(notes_col)
    ws[f"{notes_letter}1"] = "Final"
    ws[f"{notes_letter}1"].fill = header_fill
    ws[f"{notes_letter}1"].font = header_font
    ws[f"{notes_letter}1"].alignment = alignment_center
    ws[f"{notes_letter}1"].border = thin_border

    # Fila 2: Sub-títulos
    headers_row2 = ["ENROLLMENT_ID", "APODO", "NOMBRE COMPLETO", "HORA ENTRADA"]
    for i, col_name in enumerate(headers_row2, start=1):
        cell = ws.cell(row=2, column=i)
        cell.value = col_name
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = alignment_center
        cell.border = thin_border

    # Fila 2: Dias
    current_col = col_dias_start
    for day, weekday in dias_validos:
        cell = ws.cell(row=2, column=current_col)
        cell.value = f"{dias_semana[weekday]} {day:02d}"
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = alignment_center
        cell.border = thin_border
        current_col += 1
        
    # Fila 2: Notas
    cell_notes = ws.cell(row=2, column=notes_col)
    cell_notes.value = "NOTAS / OBSERVACIONES"
    cell_notes.fill = header_fill
    cell_notes.font = header_font
    cell_notes.alignment = alignment_center
    cell_notes.border = thin_border

    # Ocultar columna A (ENROLLMENT_ID)
    ws.column_dimensions['A'].hidden = True
    ws.column_dimensions['B'].width = 15
    ws.column_dimensions['C'].width = 35
    ws.column_dimensions['D'].width = 15
    for c in range(col_dias_start, col_dias_end + 1):
        ws.column_dimensions[get_column_letter(c)].width = 13
    ws.column_dimensions[notes_letter].width = 40

    # Llenar datos de estudiantes
    row = 3
    for s_data in students_data:
        # Columna A: ID Oculto
        ws.cell(row=row, column=1, value=s_data["enrollment_id"])
        ws.cell(row=row, column=2, value=s_data["nickname"])
        ws.cell(row=row, column=3, value=s_data["full_name"]).alignment = alignment_left
        ws.cell(row=row, column=4, value="07:00") # Entrada teórica
        
        # Celdas vacías para los días
        # Celdas vacías para notas
        row += 1

    # Congelar panel para poder scrollear
    ws.freeze_panes = "E3"

    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output
