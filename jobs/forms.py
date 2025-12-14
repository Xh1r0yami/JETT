from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "tasks",
            "requirements",
            "job_type",
            "location",
            "salary_range",
        ]
        widgets = {
            "tasks": forms.Textarea(attrs={"rows": 4}),
            "requirements": forms.Textarea(attrs={"rows": 4}),
        }
