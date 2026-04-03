# Librerias
from typing import Dict
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func
# Importar directorios del proyecto
from models import Attendance, Enrollment, Student, AttendanceStatus

def get_student_metrics(db: Session, student_id: str, 
                        start_date: date | None = None, 
                        end_date: date | None = None) -> Dict[str, int]:
    # Calcula el total de asistencias, faltas, retardos, etc. de un estudiante en un rango de fechas opcional
    query = db.query(Attendance.status, func.count(Attendance.id)).\
            join(Enrollment, Attendance.enrollment_id == Enrollment.id).\
            filter(Enrollment.student_id == student_id)
            
    if start_date:
        query = query.filter(Attendance.attendance_date >= start_date)
    if end_date:
        query = query.filter(Attendance.attendance_date <= end_date)
        
    results = query.group_by(Attendance.status).all()
    
    metrics = {
        "PRESENT": 0,
        "ABSENT": 0,
        "LATE": 0,
        "JUSTIFIED": 0,
        "LEFT_EARLY": 0,
        "TOTAL": 0
    }
    
    for status_enum, count in results:
        # Pydantic enum / SQLAlchemy Enum can return Enum object or value depending on config.
        # Handle both just in case.
        status_name = status_enum.name if hasattr(status_enum, "name") else status_enum
        if status_name in metrics:
            metrics[status_name] += count
            metrics["TOTAL"] += count
            
    return metrics

def get_group_metrics(db: Session, group_id: int, 
                      start_date: date | None = None, 
                      end_date: date | None = None) -> Dict[str, int]:
    # Calcula el resumen de asistencias de todo un grupo
    query = db.query(Attendance.status, func.count(Attendance.id)).\
            join(Enrollment, Attendance.enrollment_id == Enrollment.id).\
            filter(Enrollment.group_id == group_id)
            
    if start_date:
        query = query.filter(Attendance.attendance_date >= start_date)
    if end_date:
        query = query.filter(Attendance.attendance_date <= end_date)
        
    results = query.group_by(Attendance.status).all()
    
    metrics = {
        "PRESENT": 0,
        "ABSENT": 0,
        "LATE": 0,
        "JUSTIFIED": 0,
        "LEFT_EARLY": 0,
        "TOTAL": 0
    }
    
    for status_enum, count in results:
        status_name = status_enum.name if hasattr(status_enum, "name") else status_enum
        if status_name in metrics:
            metrics[status_name] += count
            metrics["TOTAL"] += count
            
    # Calcular promedios / porcentajes generales
    total = metrics["TOTAL"]
    punctuality_rate = round((metrics["PRESENT"] / total) * 100, 2) if total > 0 else 0.0
    absent_rate = round((metrics["ABSENT"] / total) * 100, 2) if total > 0 else 0.0
    
    metrics["PUNCTUALITY_PERCENTAGE"] = punctuality_rate
    metrics["ABSENT_PERCENTAGE"] = absent_rate
    
    return metrics
