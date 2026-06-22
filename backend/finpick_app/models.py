from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='diagnosis_results',
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, default='')
    income = models.CharField(max_length=50)
    expense = models.CharField(max_length=50)
    saving = models.CharField(max_length=50)
    invest = models.CharField(max_length=100)
    income_level = models.CharField(max_length=50, blank=True)
    spending_style = models.CharField(max_length=100, blank=True)
    financial_goal = models.CharField(max_length=100, blank=True)
    investment_style = models.CharField(max_length=100, blank=True)
    asset_level = models.CharField(max_length=50, blank=True)
    loan_type = models.CharField(max_length=50, blank=True)
    financial_type = models.CharField(max_length=50, blank=True)
    readiness_score = models.PositiveIntegerField(null=True, blank=True)
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    finpick_comment = models.TextField(blank=True)
    profile_scores = models.JSONField(default=dict, blank=True)
    level = models.CharField(max_length=50, default='금융 진단 완료')
    summary = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class RoadmapStep(models.Model):
    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['step_number']


class RoadmapTemplate(models.Model):
    type_code = models.CharField(max_length=50)
    level = models.PositiveIntegerField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('type_code', 'level')

    def __str__(self):
        return f'{self.type_code} {self.title}'


class RoadmapMission(models.Model):
    roadmap_template = models.ForeignKey(RoadmapTemplate, on_delete=models.CASCADE, related_name='missions')
    mission_title = models.CharField(max_length=100)
    mission_description = models.TextField(blank=True)
    category = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['roadmap_template__order', 'order']
        unique_together = ('roadmap_template', 'mission_title')

    def __str__(self):
        return self.mission_title


class UserMission(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_missions')
    mission = models.ForeignKey(RoadmapMission, on_delete=models.CASCADE, related_name='user_missions')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'mission')

    def __str__(self):
        return f'{self.user} - {self.mission}'


class ProductRecommendation(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=100)
    reason = models.TextField()
    category = models.CharField(max_length=50, default='general')

    class Meta:
        ordering = ['id']
