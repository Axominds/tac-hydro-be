from django_bolt.serializers import Serializer
from django_bolt.serializers.decorators import computed_field

from tac_hydro.extras import _serializer_instances


class JobApplicationSerializer(Serializer):
    id: int
    job: int
    first_name: str
    middle_name: str | None = None
    last_name: str
    gender: str | None = None
    phone: str | None = None
    email: str | None = None
    degree: str | None = None
    grade: str | None = None
    year_completed: str | None = None
    specialization: str | None = None
    college: str | None = None
    abilities: str | None = None
    software_proficiency: str | None = None
    employment_status: str | None = None
    experience_sector: str | None = None
    years_experience: str | None = None
    joining_date: str | None = None
    expected_salary: str | None = None
    cv_file_path: str | None = None
    cover_letter_file_path: str | None = None
    submitted_at: str | None = None
    status: str | None = None

    @computed_field
    def cv_file(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"/api/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/cv_file"

    @computed_field
    def cover_letter_file(self) -> str | None:
        instance = _serializer_instances.get(id(self))
        if instance is None:
            return None
        return f"/api/{instance._meta.app_label}/{instance._meta.model_name}/{instance.pk}/cover_letter_file"

    class Config:
        field_sets = {
            "list": ["id", "job", "first_name", "last_name", "status"],
            "detail": [
                "id",
                "job",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "phone",
                "email",
                "degree",
                "grade",
                "year_completed",
                "specialization",
                "college",
                "abilities",
                "software_proficiency",
                "employment_status",
                "experience_sector",
                "years_experience",
                "joining_date",
                "expected_salary",
                "cv_file",
                "cover_letter_file",
                "submitted_at",
                "status",
            ],
            "create": [
                "job",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "phone",
                "email",
                "degree",
                "grade",
                "year_completed",
                "specialization",
                "college",
                "abilities",
                "software_proficiency",
                "employment_status",
                "experience_sector",
                "years_experience",
                "joining_date",
                "expected_salary",
                "status",
            ],
            "update": [
                "job",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "phone",
                "email",
                "degree",
                "grade",
                "year_completed",
                "specialization",
                "college",
                "abilities",
                "software_proficiency",
                "employment_status",
                "experience_sector",
                "years_experience",
                "joining_date",
                "expected_salary",
                "status",
            ],
            "admin": [
                "id",
                "job",
                "first_name",
                "middle_name",
                "last_name",
                "gender",
                "phone",
                "email",
                "degree",
                "grade",
                "year_completed",
                "specialization",
                "college",
                "abilities",
                "software_proficiency",
                "employment_status",
                "experience_sector",
                "years_experience",
                "joining_date",
                "expected_salary",
                "cv_file_path",
                "cover_letter_file_path",
                "submitted_at",
                "status",
            ],
        }


JobApplicationListSerializer = JobApplicationSerializer.fields("list")
JobApplicationDetailSerializer = JobApplicationSerializer.fields("detail")
JobApplicationCreateSerializer = JobApplicationSerializer.fields("create")
JobApplicationUpdateSerializer = JobApplicationSerializer.fields("update")
