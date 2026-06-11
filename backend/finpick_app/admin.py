from django.contrib import admin
from .models import DiagnosisResult, RoadmapStep, ProductRecommendation

admin.site.register(DiagnosisResult)
admin.site.register(RoadmapStep)
admin.site.register(ProductRecommendation)
