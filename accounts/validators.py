import re
from django.core.exceptions import ValidationError

class StrongPasswordValidator:
    def validate(self, password, user=None):
        # Minimal 8 karakter
        if len(password) < 8:
            raise ValidationError("Password harus minimal 8 karakter.")

        # Huruf besar
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password harus mengandung huruf besar (A-Z).")

        # Huruf kecil
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password harus mengandung huruf kecil (a-z).")

        # Angka
        if not re.search(r'\d', password):
            raise ValidationError("Password harus mengandung angka (0-9).")

        # Simbol
        if not re.search(r'[\W_]', password):
            raise ValidationError("Password harus mengandung simbol.")

    def get_help_text(self):
        return (
            "Password harus minimal 8 karakter, dan mengandung huruf besar, "
            "huruf kecil, angka, dan simbol."
        )
