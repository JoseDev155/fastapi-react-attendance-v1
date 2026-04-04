# Schemas para Auth
from .auth_schema import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    ChangePasswordRequest,
    TokenResponse,
)

# Schemas para User
from .user_schema import UserBase, UserCreate, UserUpdate, UserResponse

# Schemas para Role
from .role_schema import RoleBase, RoleCreate, RoleUpdate, RoleResponse

# Schemas para Student
from .student_schema import StudentBase, StudentCreate, StudentUpdate, StudentResponse

# Schemas para AcademicCycle
from .academic_cycle_schema import (
    AcademicCycleBase,
    AcademicCycleCreate,
    AcademicCycleUpdate,
    AcademicCycleResponse,
)

# Schemas para Attendance
from .attendance_schema import (
    AttendanceBase,
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    CalculatedAttendanceResponse,
)

# Schemas para Career
from .career_schema import CareerBase, CareerCreate, CareerUpdate, CareerResponse

# Schemas para Signature
from .signature_schema import (
    SignatureBase,
    SignatureCreate,
    SignatureUpdate,
    SignatureResponse,
)

# Schemas para CareerSignature
from .career_signature_schema import (
    CareerSignatureBase,
    CareerSignatureCreate,
    CareerSignatureUpdate,
    CareerSignatureResponse,
)

# Schemas para Enrollment
from .enrollment_schema import (
    EnrollmentBase,
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
)

# Schemas para Group
from .group_schema import GroupBase, GroupCreate, GroupUpdate, GroupResponse

# Schemas para Schedule
from .schedule_schema import ScheduleBase, ScheduleCreate, ScheduleUpdate, ScheduleResponse

__all__ = [
    # Auth
    "LoginRequest",
    "RegisterRequest",
    "RefreshTokenRequest",
    "ChangePasswordRequest",
    "TokenResponse",
    # User
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Role
    "RoleBase",
    "RoleCreate",
    "RoleUpdate",
    "RoleResponse",
    # Student
    "StudentBase",
    "StudentCreate",
    "StudentUpdate",
    "StudentResponse",
    # AcademicCycle
    "AcademicCycleBase",
    "AcademicCycleCreate",
    "AcademicCycleUpdate",
    "AcademicCycleResponse",
    # Attendance
    "AttendanceBase",
    "AttendanceCreate",
    "AttendanceUpdate",
    "AttendanceResponse",
    "CalculatedAttendanceResponse",
    # Career
    "CareerBase",
    "CareerCreate",
    "CareerUpdate",
    "CareerResponse",
    # Signature
    "SignatureBase",
    "SignatureCreate",
    "SignatureUpdate",
    "SignatureResponse",
    # CareerSignature
    "CareerSignatureBase",
    "CareerSignatureCreate",
    "CareerSignatureUpdate",
    "CareerSignatureResponse",
    # Enrollment
    "EnrollmentBase",
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    # Group
    "GroupBase",
    "GroupCreate",
    "GroupUpdate",
    "GroupResponse",
    # Schedule
    "ScheduleBase",
    "ScheduleCreate",
    "ScheduleUpdate",
    "ScheduleResponse",
]
