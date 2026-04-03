# Academic Cycle Service
from .academic_cycle_service import (
    get_all_service as get_all_academic_cycles,
    search_by_id_service as search_academic_cycle_by_id,
    search_by_name_service as search_academic_cycle_by_name,
    create_academic_cycle_service,
    update_academic_cycle_service,
    destroy_academic_cycle_service,
)

# Attendance Service
from .attendance_service import (
    get_all_service as get_all_attendances,
    search_by_id_service as search_attendance_by_id,
    create_attendance_service,
    update_attendance_service,
    destroy_attendance_service,
)

# Auth Service
from .auth_service import (
    login_auth_service,
    register_auth_service,
    refresh_token_auth_service,
    change_password_auth_service,
    get_current_user_info_service
)

# Career Service
from .career_service import (
    get_all_service as get_all_careers,
    search_by_id_service as search_career_by_id,
    search_by_name_service as search_careers_by_name,
    create_career_service,
    update_career_service,
    delete_career_service,
    reactivate_career_service,
    destroy_career_service,
)

# Career Signature Service
from .career_signature_service import (
    get_all_service as get_all_career_signatures,
    search_by_id_service as search_career_signature_by_id,
    create_career_signature_service,
    update_career_signature_service,
    destroy_career_signature_service,
)

# Enrollment Service
from .enrollment_service import (
    get_all_service as get_all_enrollments,
    search_by_id_service as search_enrollment_by_id,
    search_by_date_service as search_enrollments_by_date,
    create_enrollment_service,
    update_enrollment_service,
    destroy_enrollment_service,
)

# Group Service
from .group_service import (
    get_all_service as get_all_groups,
    search_by_id_service as search_group_by_id,
    search_by_name_service as search_groups_by_name,
    create_group_service,
    update_group_service,
    destroy_group_service,
)

# Role Service
from .role_service import (
    get_all_service as get_all_roles,
    search_by_id_service as search_role_by_id,
    search_by_name_service as search_roles_by_name,
    create_role_service,
    update_role_service,
    delete_role_service,
    reactivate_role_service,
    destroy_role_service,
)

# Schedule Service
from .schedule_service import (
    get_all_service as get_all_schedules,
    search_by_id_service as search_schedule_by_id,
    search_by_day_service as search_schedules_by_day,
    create_schedule_service,
    update_schedule_service,
    destroy_schedule_service,
)

# Signature Service
from .signature_service import (
    get_all_service as get_all_signatures,
    search_by_id_service as search_signature_by_id,
    search_by_name_service as search_signatures_by_name,
    create_signature_service,
    update_signature_service,
    destroy_signature_service,
)

# Student Service
from .student_service import (
    get_all_service as get_all_students,
    search_by_id_service as search_student_by_id,
    search_by_name_service as search_students_by_name,
    search_by_email_service as search_students_by_email,
    create_student_service,
    update_student_service,
    destroy_student_service,
)

# User Service
from .user_service import (
    get_all_service as get_all_users,
    search_by_id_service as search_user_by_id,
    search_by_id_or_email_service as search_users_by_id_or_email,
    search_by_name_service as search_user_by_name,
    create_user_service,
    update_user_service,
    delete_user_service,
    reactivate_user_service,
    destroy_user_service,
)

__all__ = [
    # Academic Cycle
    "get_all_academic_cycles",
    "search_academic_cycle_by_id",
    "search_academic_cycle_by_name",
    "create_academic_cycle_service",
    "update_academic_cycle_service",
    "destroy_academic_cycle_service",
    # Attendance
    "get_all_attendances",
    "search_attendance_by_id",
    "create_attendance_service",
    "update_attendance_service",
    "destroy_attendance_service",
    # Auth
    "login_auth_service",
    "register_auth_service",
    "refresh_token_auth_service",
    "change_password_auth_service",
    "get_current_user_info_service",
    # Career
    "get_all_careers",
    "search_career_by_id",
    "search_careers_by_name",
    "create_career_service",
    "update_career_service",
    "delete_career_service",
    "reactivate_career_service",
    "destroy_career_service",
    # Career Signature
    "get_all_career_signatures",
    "search_career_signature_by_id",
    "create_career_signature_service",
    "update_career_signature_service",
    "destroy_career_signature_service",
    # Enrollment
    "get_all_enrollments",
    "search_enrollment_by_id",
    "search_enrollments_by_date",
    "create_enrollment_service",
    "update_enrollment_service",
    "destroy_enrollment_service",
    # Group
    "get_all_groups",
    "search_group_by_id",
    "search_groups_by_name",
    "create_group_service",
    "update_group_service",
    "destroy_group_service",
    # Role
    "get_all_roles",
    "search_role_by_id",
    "search_roles_by_name",
    "create_role_service",
    "update_role_service",
    "delete_role_service",
    "reactivate_role_service",
    "destroy_role_service",
    # Schedule
    "get_all_schedules",
    "search_schedule_by_id",
    "search_schedules_by_day",
    "create_schedule_service",
    "update_schedule_service",
    "destroy_schedule_service",
    # Signature
    "get_all_signatures",
    "search_signature_by_id",
    "search_signatures_by_name",
    "create_signature_service",
    "update_signature_service",
    "destroy_signature_service",
    # Student
    "get_all_students",
    "search_student_by_id",
    "search_students_by_name",
    "search_students_by_email",
    "create_student_service",
    "update_student_service",
    "destroy_student_service",
    # User
    "get_all_users",
    "search_user_by_id",
    "search_users_by_id_or_email",
    "search_user_by_name",
    "create_user_service",
    "update_user_service",
    "delete_user_service",
    "reactivate_user_service",
    "destroy_user_service",
]
