from django import forms
from .models import Application
from django.core.exceptions import ValidationError

MAX_CV_SIZE = 2 * 1024 * 1024  # 2 MB

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cv"]

    def clean_cv(self):
        cv = self.cleaned_data.get("cv")

        if not cv:
            return cv

        if cv.size > MAX_CV_SIZE:
            raise ValidationError(
                "Ukuran file terlalu besar. Maksimal 2 MB."
            )

        if not cv.name.lower().endswith(".pdf"):
            raise ValidationError(
                "Format file tidak valid. Harus PDF."
            )

        return cv
