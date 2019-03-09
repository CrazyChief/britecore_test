from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class RiskType(models.Model):
    type_name = models.CharField(_('Type Name'), max_length=120, unique=True)
    schema = JSONField()
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Risk Type')
        verbose_name_plural = _('Risk Types')

    def __str__(self):
        return f'Risk Type: {self.type_name}'

    def is_risk_type_active(self):
        return self.is_active

    is_risk_type_active.admin_order_field = 'is_active'
    is_risk_type_active.boolean = True
    is_risk_type_active.short_description = _('Is active?')


class Risk(models.Model):
    risk_type = models.ForeignKey(
        RiskType, on_delete=models.SET_NULL, null=True,
        verbose_name=_('Risk Type'))
    risk_data = JSONField()
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Updated'))

    class Meta:
        verbose_name = _('Risk')
        verbose_name_plural = _('Risks')
