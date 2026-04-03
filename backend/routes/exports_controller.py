from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from models import User, Enrollment, Student
from utils import get_current_admin_user
from exports import generate_attendance_template

exports_controller = APIRouter()

@exports_controller.get("/exports/template/group/{group_id}", tags=["exports"])
async def export_group_template(group_id: int, year: int, month: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    enrollments = db.query(Enrollment).filter(Enrollment.group_id == group_id).all()
    students_data = []
    for enr in enrollments:
        student = db.query(Student).filter(Student.id == enr.student_id).first()
        if student:
            students_data.append({
                "enrollment_id": enr.id,
                "nickname": student.nickname,
                "full_name": f"{student.first_name} {student.last_name}"
            })
            
    try:
        excel_stream = generate_attendance_template(year, month, students_data)
        return StreamingResponse(
            excel_stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=attendance_template_{year}_{month:02d}.xlsx"}
        )
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
