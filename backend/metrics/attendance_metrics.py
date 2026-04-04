# Librerias
from typing import Dict, Any
from datetime import date, time, timedelta
from sqlalchemy.orm import Session
# Importar directorios del proyecto
from models import Attendance, Enrollment, Schedule


# Clasificación dinamica basada en Schedule

def _time_to_minutes(t: time) -> int:
    # Convierte un objeto time en minutos totales desde medianoche
    return t.hour * 60 + t.minute


def classify_attendance(arrival_time: time | None, schedule: Schedule | None) -> str:
    """
    Calcula el estado de asistencia comparando la hora de llegada
    contra las reglas del horario (Schedule).

    Reglas:
    - Sin arrival_time (NULL)          → ABSENT
    - Sin Schedule para ese día        → ABSENT (no hay clase)
    - arrival_time <= start_time       → PRESENT
    - arrival_time <= start_time + minutes_to_be_late → PRESENT (dentro de tolerancia)
    - arrival_time > start_time + minutes_to_be_late  → LATE
    - arrival_time > end_time          → LEFT_EARLY (llegó pero ya terminó)

    Nota: JUSTIFIED no puede derivarse de la hora; se infiere si las notas
    comienzan con "JUSTIFICADO:" (prefijo reservado).
    """
    if arrival_time is None:
        return "ABSENT"
    
    if schedule is None:
        return "ABSENT"

    arrival_mins = _time_to_minutes(arrival_time)
    start_mins   = _time_to_minutes(schedule.start_time)
    end_mins     = _time_to_minutes(schedule.end_time)
    tolerance    = schedule.minutes_to_be_late

    if arrival_mins > end_mins:
        return "LEFT_EARLY"
    elif arrival_mins <= (start_mins + tolerance):
        return "PRESENT"
    else:
        return "LATE"


def _get_schedule_for_attendance(db: Session, enrollment_id: int, attendance_date: date) -> Schedule | None:
    """
    Busca el Schedule del grupo al que pertenece el enrollment
    que coincida con el día de la semana de attendance_date.
    El campo day_of_week sigue la convención de Python: 0=Lunes … 6=Domingo.
    """
    weekday = attendance_date.weekday()  # 0=Lun, 6=Dom

    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        return None

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.group_id == enrollment.group_id,
            Schedule.day_of_week == weekday
        )
        .first()
    )
    return schedule


# ──────────────────────────────────────────────
# Funciones de métricas
# ──────────────────────────────────────────────

def get_student_metrics(
    db: Session,
    student_id: str,
    start_date: date | None = None,
    end_date: date | None = None
) -> Dict[str, Any]:
    """
    Calcula el total de asistencias, faltas, retardos, etc.
    de un estudiante en un rango de fechas opcional.
    El estado se deriva dinámicamente del Schedule del grupo.
    """
    query = (
        db.query(Attendance)
        .join(Enrollment, Attendance.enrollment_id == Enrollment.id)
        .filter(Enrollment.student_id == student_id)
    )

    if start_date:
        query = query.filter(Attendance.attendance_date >= start_date)
    if end_date:
        query = query.filter(Attendance.attendance_date <= end_date)

    records = query.all()

    metrics: Dict[str, Any] = {
        "PRESENT": 0,
        "ABSENT": 0,
        "LATE": 0,
        "JUSTIFIED": 0,
        "LEFT_EARLY": 0,
        "TOTAL": 0
    }

    for record in records:
        # Detectar justificados por convención de notas
        if record.notes and record.notes.upper().startswith("JUSTIFICADO:"):
            status = "JUSTIFIED"
        else:
            schedule = _get_schedule_for_attendance(db, record.enrollment_id, record.attendance_date)
            status = classify_attendance(record.arrival_time, schedule)

        metrics[status] += 1
        metrics["TOTAL"] += 1

    return metrics


def get_group_metrics(
    db: Session,
    group_id: str,
    start_date: date | None = None,
    end_date: date | None = None
) -> Dict[str, Any]:
    """
    Calcula el resumen de asistencias de todo un grupo.
    El estado se deriva dinámicamente del Schedule del grupo.
    """
    query = (
        db.query(Attendance)
        .join(Enrollment, Attendance.enrollment_id == Enrollment.id)
        .filter(Enrollment.group_id == group_id)
    )

    if start_date:
        query = query.filter(Attendance.attendance_date >= start_date)
    if end_date:
        query = query.filter(Attendance.attendance_date <= end_date)

    records = query.all()

    metrics: Dict[str, Any] = {
        "PRESENT": 0,
        "ABSENT": 0,
        "LATE": 0,
        "JUSTIFIED": 0,
        "LEFT_EARLY": 0,
        "TOTAL": 0
    }

    for record in records:
        if record.notes and record.notes.upper().startswith("JUSTIFICADO:"):
            status = "JUSTIFIED"
        else:
            schedule = _get_schedule_for_attendance(db, record.enrollment_id, record.attendance_date)
            status = classify_attendance(record.arrival_time, schedule)

        metrics[status] += 1
        metrics["TOTAL"] += 1

    # Calcular porcentajes globales
    total = metrics["TOTAL"]
    metrics["PUNCTUALITY_PERCENTAGE"] = round((metrics["PRESENT"] / total) * 100, 2) if total > 0 else 0.0
    metrics["ABSENT_PERCENTAGE"]      = round((metrics["ABSENT"]  / total) * 100, 2) if total > 0 else 0.0

    return metrics
