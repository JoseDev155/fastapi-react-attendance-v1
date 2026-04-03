# Academic Cycle Repository
from .academic_cycle_repository import (
    get_all as academic_cycle_get_all,
    search_by_id as academic_cycle_search_by_id,
    search_by_name as academic_cycle_search_by_name,
    create as academic_cycle_create,
    update as academic_cycle_update,
    destroy as academic_cycle_destroy,
)

# Attendance Repository
from .attendance_repository import (
    get_all as attendance_get_all,
    search_by_id as attendance_search_by_id,
    search_by_arrival as attendance_search_by_arrival,
    search_by_enrollment_and_date as attendance_search_by_enrollment_and_date,
    create as attendance_create,
    update as attendance_update,
    destroy as attendance_destroy,
)

# Career Repository
from .career_repository import (
    get_all as career_get_all,
    search_by_id as career_search_by_id,
    search_by_name as career_search_by_name,
    create as career_create,
    update as career_update,
    reactivate as career_reactivate,
    destroy as career_destroy,
    deactivate as career_deactivate,
)

# Career Signature Repository
from .career_signature_repository import (
    get_all as career_signature_get_all,
    search_by_id as career_signature_search_by_id,
    create as career_signature_create,
    update as career_signature_update,
    destroy as career_signature_destroy,
)

# Enrollment Repository
from .enrollment_repository import (
    get_all as enrollment_get_all,
    search_by_id as enrollment_search_by_id,
    search_by_date as enrollment_search_by_date,
    create as enrollment_create,
    update as enrollment_update,
    destroy as enrollment_destroy,
)

# Group Repository
from .group_repository import (
    get_all as group_get_all,
    search_by_id as group_search_by_id,
    search_by_name as group_search_by_name,
    create as group_create,
    update as group_update,
    destroy as group_destroy,
)

# Role Repository
from .role_repository import (
    get_all as role_get_all,
    search_by_id as role_search_by_id,
    search_by_name as role_search_by_name,
    create as role_create,
    update as role_update,
    reactivate as role_reactivate,
    destroy as role_destroy,
    deactivate as role_deactivate,
)

# Schedule Repository
from .schedule_repository import (
    get_all as schedule_get_all,
    search_by_id as schedule_search_by_id,
    search_by_day as schedule_search_by_day,
    create as schedule_create,
    update as schedule_update,
    destroy as schedule_destroy,
)

# Signature Repository
from .signature_repository import (
    get_all as signature_get_all,
    search_by_id as signature_search_by_id,
    search_by_name as signature_search_by_name,
    create as signature_create,
    update as signature_update,
    destroy as signature_destroy,
)

# Student Repository
from .student_repository import (
    get_all as student_get_all,
    search_by_id as student_search_by_id,
    search_by_name as student_search_by_name,
    search_by_email as student_search_by_email,
    create as student_create,
    update as student_update,
    destroy as student_destroy,
)

# User Repository
from .user_repository import (
    get_all as user_get_all,
    search_by_id as user_search_by_id,
    search_by_name as user_search_by_name,
    search_by_id_or_email as user_search_by_id_or_email,
    create as user_create,
    update as user_update,
    reactivate as user_reactivate,
    destroy as user_destroy,
    deactivate as user_deactivate,
)

__all__ = [
    # Academic Cycle
    "academic_cycle_get_all",
    "academic_cycle_search_by_id",
    "academic_cycle_search_by_name",
    "academic_cycle_create",
    "academic_cycle_update",
    "academic_cycle_destroy",
    # Attendance
    "attendance_get_all",
    "attendance_search_by_id",
    "attendance_search_by_arrival",
    "attendance_search_by_enrollment_and_date",
    "attendance_create",
    "attendance_update",
    "attendance_destroy",
    # Career
    "career_get_all",
    "career_search_by_id",
    "career_search_by_name",
    "career_create",
    "career_update",
    "career_destroy",
    "career_reactivate",
    "career_deactivate",
    # Career Signature
    "career_signature_get_all",
    "career_signature_search_by_id",
    "career_signature_create",
    "career_signature_update",
    "career_signature_destroy",
    # Enrollment
    "enrollment_get_all",
    "enrollment_search_by_id",
    "enrollment_search_by_date",
    "enrollment_create",
    "enrollment_update",
    "enrollment_destroy",
    # Group
    "group_get_all",
    "group_search_by_id",
    "group_search_by_name",
    "group_create",
    "group_update",
    "group_destroy",
    # Role
    "role_get_all",
    "role_search_by_id",
    "role_search_by_name",
    "role_create",
    "role_update",
    "role_reactivate",
    "role_destroy",
    "role_deactivate",
    # Schedule
    "schedule_get_all",
    "schedule_search_by_id",
    "schedule_search_by_day",
    "schedule_create",
    "schedule_update",
    "schedule_destroy",
    # Signature
    "signature_get_all",
    "signature_search_by_id",
    "signature_search_by_name",
    "signature_create",
    "signature_update",
    "signature_destroy",
    # Student
    "student_get_all",
    "student_search_by_id",
    "student_search_by_name",
    "student_search_by_email",
    "student_create",
    "student_update",
    "student_destroy",
    # User
    "user_get_all",
    "user_search_by_id",
    "user_search_by_name",
    "user_search_by_id_or_email",
    "user_create",
    "user_update",
    "user_reactivate",
    "user_destroy",
    "user_deactivate",
]
