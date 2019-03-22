from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
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


@receiver(post_save, sender=RiskType)
def schema_update(sender, instance, **kwargs):
    if kwargs['created'] is False:
        risks = Risk.objects.filter(risk_type__id=instance.id)
        for risk in risks:
            schema_len = len(instance.schema)
            risk_data_len = len(risk.risk_data)
            r = risk.risk_data
            if schema_len == risk_data_len:
                for i, part in enumerate(instance.schema):
                    # makes updates to schema in case comparison is False
                    if part['field_name'] != r[i]['field_name']:
                        r[i]['field_name'] = part['field_name']
                    if part['field_type'] != r[i]['field_type']:
                        r[i]['field_type'] = part['field_type']
                        r[i]['value'] = None
                        r[i]['optionDisabled'] = part['optionDisabled']
                        r[i]['is_required'] = part['is_required']
                        r[i]['options'] = part['options']
            elif schema_len != risk_data_len:
                temp_schema = list(instance.schema)
                if schema_len > risk_data_len:
                    for i, part in enumerate(temp_schema):
                        if i > risk_data_len - 1:
                            # add new part to existent schema
                            part.update({'value': None})
                            r.append(part)
                        else:
                            if part['field_name'] != r[i]['field_name']:
                                r[i]['field_name'] = part['field_name']
                            if part['field_type'] != r[i]['field_type']:
                                r[i]['field_type'] = part['field_type']
                                r[i]['value'] = None
                                r[i]['optionDisabled'] = part['optionDisabled']
                                r[i]['is_required'] = part['is_required']
                                r[i]['options'] = part['options']
                elif schema_len < risk_data_len:
                    for i, part in enumerate(temp_schema):
                        if i + 1 == risk_data_len - 1:
                            # remove items not listed in new risk type schema
                            r = r[:max(
                                risk_data_len - 1, 0)] + r[risk_data_len:]
                            risk.risk_data = r
                        else:
                            if part['field_name'] != r[i]['field_name']:
                                r[i]['field_name'] = part['field_name']
                            if part['field_type'] != r[i]['field_type']:
                                r[i]['field_type'] = part['field_type']
                                r[i]['value'] = None
                                r[i]['optionDisabled'] = part['optionDisabled']
                                r[i]['is_required'] = part['is_required']
                                r[i]['options'] = part['options']
            risk.save()
