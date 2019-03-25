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


def update_pieces(part, risk_field):
    # Update dada in appropriate field
    if part['field_name'] != risk_field['field_name']:
        risk_field['field_name'] = part['field_name']
    if part['field_type'] != risk_field['field_type']:
        risk_field['field_type'] = part['field_type']
        risk_field['value'] = None
        risk_field['optionDisabled'] = part['optionDisabled']
        risk_field['is_required'] = part['is_required']
        risk_field['options'] = part['options']
    return risk_field


@receiver(post_save, sender=RiskType)
def schema_update(sender, instance, **kwargs):
    if kwargs['created'] is False:
        risks = Risk.objects.filter(risk_type__id=instance.id)
        for risk in risks:
            schema_len = len(instance.schema)
            risk_data_len = len(risk.risk_data)
            r = risk.risk_data
            if schema_len >= risk_data_len:
                print('schema_len > risk_data_len cond')
                i = 0
                while i <= schema_len - 1:
                    part = instance.schema[i]
                    if i > risk_data_len - 1:
                        # add new part to existent schema
                        part = instance.schema[i]
                        part.update({'value': None})
                        r.append(part)
                        i += 1
                        risk_data_len += 1
                    else:
                        if part['field_id'] != r[i]['field_id']:
                            # Remove field from risk_data
                            r.pop(i)
                            risk_data_len -= 1
                        else:
                            r[i] = update_pieces(part, r[i])
                            i += 1
            elif schema_len < risk_data_len:
                keys = [key['field_id'] for key in instance.schema]
                i = 0
                while i <= risk_data_len - 1:
                    if i == risk_data_len:
                        break
                    if r[i]['field_id'] not in keys:
                        # Remove field from risk_data
                        r.pop(i)
                        risk_data_len -= 1
                    else:
                        i += 1
                for i, part in enumerate(instance.schema):
                    if part['field_id'] == r[i]['field_id']:
                        update_pieces(part, r[i])
            risk.risk_data = r
            risk.save()
