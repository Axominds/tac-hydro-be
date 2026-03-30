from django.db import models


class PartnershipRoadmapSection(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True)

    class Meta:
        db_table = "partnership_roadmap_sections"

    def __str__(self) -> str:
        return self.title


class PartnershipRoadmapStep(models.Model):
    section = models.ForeignKey(
        PartnershipRoadmapSection,
        on_delete=models.CASCADE,
        related_name="steps",
    )
    milestone = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon_key = models.CharField(max_length=64)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "partnership_roadmap_steps"
        ordering = ["order", "milestone"]

    def __str__(self) -> str:
        return self.title


class InitiateSynergySection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cta_text = models.CharField(max_length=255, blank=True)
    cta_note = models.TextField(blank=True)

    class Meta:
        db_table = "initiate_synergy_sections"

    def __str__(self) -> str:
        return self.title


class JobType(models.TextChoices):
    FULL_TIME = "Full Time", "Full Time"
    INTERNSHIP = "Internship", "Internship"
    INDEPENDENT_CONSULTANT = "Independent Consultant", "Independent Consultant"


class JobCategory(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "job_categories"
        ordering = ["order", "name"]

    def __str__(self) -> str:
        return self.name


class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(JobCategory, on_delete=models.PROTECT, related_name="jobs")
    type = models.CharField(max_length=32, choices=JobType.choices)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    responsibilities = models.JSONField(default=list, blank=True)
    qualifications = models.JSONField(default=list, blank=True)
    is_open = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "job_postings"

    def __str__(self) -> str:
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name="applications")
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=64, blank=True)
    phone = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    degree = models.CharField(max_length=255, blank=True)
    grade = models.CharField(max_length=255, blank=True)
    year_completed = models.CharField(max_length=16, blank=True)
    specialization = models.CharField(max_length=255, blank=True)
    college = models.CharField(max_length=255, blank=True)
    abilities = models.TextField(blank=True)
    software_proficiency = models.TextField(blank=True)
    employment_status = models.CharField(max_length=255, blank=True)
    experience_sector = models.CharField(max_length=255, blank=True)
    years_experience = models.CharField(max_length=32, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    expected_salary = models.CharField(max_length=64, blank=True)
    cv_file = models.FileField(upload_to="contact_us/applications/cv", blank=True)
    cover_letter_file = models.FileField(upload_to="contact_us/applications/cover", blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = "job_applications"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
