from rest_framework import serializers

from contact_us.models import JobApplication


class JobApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ["id", "job_id", "first_name", "last_name", "email", "submitted_at"]


class JobApplicationDetailSerializer(JobApplicationListSerializer):
    cv_file = serializers.SerializerMethodField()
    cover_letter_file = serializers.SerializerMethodField()

    class Meta(JobApplicationListSerializer.Meta):
        fields = [
            "id",
            "job_id",
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
        ]

    def get_cv_file(self, obj):
        if not obj.cv_file:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.cv_file.url)
        return obj.cv_file.url

    def get_cover_letter_file(self, obj):
        if not obj.cover_letter_file:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.cover_letter_file.url)
        return obj.cover_letter_file.url


class JobApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "job_id",
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
        ]

    def validate(self, data):
        job = data.get("job") or data.get("job_id")
        if not job:
            job_id = self.initial_data.get("job_id")
            if job_id:
                from contact_us.models import JobPosting
                job = JobPosting.objects.filter(id=job_id).first()

        if not job:
            raise serializers.ValidationError({"job_id": "Job is required."})

        data["job"] = job

        required_always = [
            "first_name", "last_name", "gender", "phone", "email",
            "degree", "grade", "year_completed", "specialization", "college",
            "experience_sector", "years_experience"
        ]
        
        required_conditional = [
            "abilities", "software_proficiency", "employment_status",
            "joining_date", "expected_salary"
        ]

        errors = {}
        for field in required_always:
            if not self.initial_data.get(field):
                errors[field] = "This field is required."

        if not self.initial_data.get("cv_file"):
            errors["cv_file"] = "CV file is required."
        if not self.initial_data.get("cover_letter_file"):
            errors["cover_letter_file"] = "Cover letter is required."

        if job.type != "Independent Consultant":
            for field in required_conditional:
                if not self.initial_data.get(field):
                    errors[field] = "This field is required."

        if errors:
            raise serializers.ValidationError(errors)

        return data


class FlexibleDateField(serializers.DateField):
    def to_internal_value(self, value):
        if value == "" or value is None:
            return None
        return super().to_internal_value(value)


class JobApplicationUpdateSerializer(serializers.ModelSerializer):
    joining_date = FlexibleDateField(required=False, allow_null=True)

    class Meta:
        model = JobApplication
        fields = [
            "first_name", "middle_name", "last_name", "gender", "phone", "email",
            "degree", "grade", "year_completed", "specialization", "college",
            "abilities", "software_proficiency", "employment_status",
            "experience_sector", "years_experience", "joining_date", "expected_salary",
        ]
        extra_kwargs = {field: {"required": False} for field in fields}

    def validate(self, data):
        job = self.instance.job if self.instance else None
        errors = {}

        required_always = [
            "first_name", "last_name", "gender", "phone", "email",
            "degree", "grade", "year_completed", "specialization", "college",
            "experience_sector", "years_experience",
        ]

        for field in required_always:
            if field in self.initial_data and not self.initial_data.get(field):
                errors[field] = "This field is required."

        if job and job.type != "Independent Consultant":
            for field in ["abilities", "software_proficiency", "employment_status", "joining_date", "expected_salary"]:
                if field in self.initial_data and not self.initial_data.get(field):
                    errors[field] = "This field is required for this position."

        if errors:
            raise serializers.ValidationError(errors)

        return data
