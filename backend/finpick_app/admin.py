from django.contrib import admin
from .models import AiProductRecommendation, DailyFinancialTip, DiagnosisResult, RoadmapStep, ProductRecommendation

admin.site.register(AiProductRecommendation)
admin.site.register(DailyFinancialTip)
admin.site.register(DiagnosisResult)
admin.site.register(RoadmapStep)
admin.site.register(ProductRecommendation)
