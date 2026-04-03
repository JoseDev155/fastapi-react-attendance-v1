# Academic Cycle Router
from .academic_cycle_controller import academic_cycle_controller

# Attendance Router
from .attendance_controller import attendance_controller

# Auth Router
from .auth_controller import auth_controller

# Career Router
from .career_controller import career_controller

# Career Signature Router
from .career_signature_controller import career_signature_controller

# Enrollment Router
from .enrollment_controller import enrollment_controller

# Group Router
from .group_controller import group_controller

# Health Router
from .health_controller import health_controller

# Role Router
from .role_controller import role_controller

# Schedule Router
from .schedule_controller import schedule_controller

# Signature Router
from .signature_controller import signature_controller

# Student Router
from .student_controller import student_controller

# User Router
from .user_controller import user_controller

__all__ = [
    "academic_cycle_controller",
    "attendance_controller",
    "auth_controller",
    "career_controller",
    "career_signature_controller",
    "enrollment_controller",
    "group_controller",
    "health_controller",
    "role_controller",
    "schedule_controller",
    "signature_controller",
    "student_controller",
    "user_controller",
]
