from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import (
    MinimumLengthValidator as BaseMinimumLengthValidator,
    UserAttributeSimilarityValidator as BaseUserAttributeSimilarityValidator,
    NumericPasswordValidator as BaseNumericPasswordValidator,
    CommonPasswordValidator as BaseCommonPasswordValidator
)
import gzip
import os

class MinimumLengthValidator(BaseMinimumLengthValidator):
    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Esta senha é muito curta. Deve conter pelo menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos %(min_length)d caracteres."
        ) % {'min_length': self.min_length}

class CustomCommonPasswordValidator(BaseCommonPasswordValidator):
    def __init__(self, password_list_path=None):
        self.passwords = set()
        if password_list_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            password_list_path = os.path.join(base_dir, 'common-passwords.txt.gz')
        try:
            with gzip.open(password_list_path, 'rt', encoding='utf-8') as f:
                for line in f:
                    self.passwords.add(line.strip().lower())
        except FileNotFoundError:
            print(f"Warning: Password list file not found at {password_list_path}")

    def validate(self, password, user=None):
        if password.lower() in self.passwords:
            raise ValidationError(
                _("Esta senha é muito comum."),
                code='password_too_common',
            )

    def get_help_text(self):
        return _("Sua senha não pode ser uma senha comumente usada.")

class NumericPasswordValidator(BaseNumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("Esta senha é inteiramente numérica."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("Sua senha não pode ser inteiramente numérica.")

class CustomUserAttributeSimilarityValidator(BaseUserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        if user:
            user_attributes = [
                user.username,
                user.email,
            ]
            for attribute in user_attributes:
                if attribute and password.lower() in attribute.lower():
                    raise ValidationError(
                        _("Sua senha é muito similar a suas outras informações pessoais."),
                        code='password_too_similar',
                    )

    def get_help_text(self):
        return _("Sua senha não pode ser muito similar às suas outras informações pessoais.")
