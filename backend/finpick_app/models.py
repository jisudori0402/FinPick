from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    job = models.CharField(max_length=100, blank=True)
    monthly_income = models.PositiveIntegerField(null=True, blank=True)
    monthly_expense = models.PositiveIntegerField(null=True, blank=True)
    residence_type = models.CharField(max_length=50, blank=True)
    saving_status = models.CharField(max_length=50, blank=True)
    invest_experience = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class DiagnosisResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diagnosis_results', null=True, blank=True)
    name = models.CharField(max_length=100, default='김민지')
    income = models.CharField(max_length=50)
    expense = models.CharField(max_length=50)
    saving = models.CharField(max_length=50)
    invest = models.CharField(max_length=30)
    level = models.CharField(max_length=50, default='금융 새싹 🌱')
    summary = models.TextField(default='투자보다 비상금과 저축 습관 형성이 우선입니다.')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class RoadmapStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['step_number']


class ProductRecommendation(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    reason = models.TextField()
    category = models.CharField(max_length=50, default='general')

    class Meta:
        ordering = ['id']
