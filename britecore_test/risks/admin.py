from django.contrib import admin

from .models import RiskType, Risk


@admin.register(RiskType)
class RiskTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'is_risk_type_active', 'created', 'updated')


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    pass
