from typing import Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from metrics import get_group_metrics, get_student_metrics
from models import Group, Student, Enrollment

def generate_monthly_group_report(db: Session, group_id: int, year: int, month: int) -> Dict[str, Any]:
    """
    Genera un reporte detallado para un grupo en un mes específico.
    """
    from calendar import monthrange
    _, last_day = monthrange(year, month)
    
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)
    
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return {"error": "Group not found"}
        
    group_stats = get_group_metrics(db, group_id, start_date, end_date)
    
    # Detallar por estudiante
    student_details = []
    enrollments = db.query(Enrollment).filter(Enrollment.group_id == group_id).all()
    for enr in enrollments:
        student = db.query(Student).filter(Student.id == enr.student_id).first()
        if not student:
            continue
            
        student_stats = get_student_metrics(db, student.id, start_date, end_date)
        student_details.append({
            "student_id": student.id,
            "nickname": student.nickname,
            "full_name": f"{student.first_name} {student.last_name}",
            "stats": student_stats
        })
        
    return {
        "report_type": "monthly_group_report",
        "group_name": group.name,
        "year": year,
        "month": month,
        "global_stats": group_stats,
        "students": student_details
    }
