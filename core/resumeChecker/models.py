from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Resume(models.Model):
    resume = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    filename = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):
        if not self.filename and self.resume:
            self.filename = self.resume.name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.filename or f"Resume {self.id}"


class JobDescription(models.Model):
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.job_title


class AnalysisResult(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    analyzed_at = models.DateTimeField(auto_now_add=True)

    # Analysis results
    rank = models.IntegerField()  # 0-100
    skills = models.JSONField()  # List of skills
    total_experience = models.CharField(max_length=100)  # "X years" or "no experience mention"
    project_categories = models.JSONField()  # List of project categories
    resume_summary = models.TextField(blank=True)  # LLM-generated summary

    # Raw analysis data for future use
    raw_data = models.JSONField()

    class Meta:
        ordering = ['-analyzed_at']

    def __str__(self):
        return f"Analysis: {self.resume.filename} vs {self.job_description.job_title}"

    @property
    def match_percentage(self):
        return self.rank