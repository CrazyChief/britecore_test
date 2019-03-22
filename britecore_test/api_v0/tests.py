from datetime import timedelta, date
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from risks.models import RiskType, Risk

from .constants import TEST_SCHEMA, TEST_RISK_DATA
from .serializers import RiskTypeSerializer, RiskSerializer


class RiskTypeTests(APITestCase):
    """
    Provide tests for RiskType:
    1) creating RiskType object;
    2) getting details of RiskType object;
    3) updating RiskType object for type_name;
    4) updating RiskType object for schema param;
    """

    def create_risk_type(self):
        risk_type = RiskType.objects.create(
            type_name='New Risk Type',
            schema=TEST_SCHEMA
        )
        risk_type.save()

        return risk_type

    def test_create_risk_type(self):
        """
        Ensure we can create a new RiskType object.
        """
        url = r'/api/v0/risk-types/'
        data = {
            'type_name': 'New Risk Type',
            'schema': TEST_SCHEMA
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskType.objects.count(), 1)
        self.assertEqual(RiskType.objects.get().type_name, 'New Risk Type')

    def test_can_get_risk_type_details(self):
        """
        Create RiskType object and try to get it.
        """
        risk_type = self.create_risk_type()
        response = self.client.get(f'/api/v0/risk-types/{risk_type.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         RiskTypeSerializer(instance=risk_type).data)

    def test_can_update_risk_type_name(self):
        """
        Create RiskType object and try to update its type_name.
        """
        risk_type = self.create_risk_type()
        response = self.client.put(
            f'/api/v0/risk-types/{risk_type.id}/',
            data={
                'type_name': 'House',
                'schema': risk_type.schema,
            }, format='json')
        risk_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(risk_type.type_name, 'House')

    def test_can_update_risk_type_schema(self):
        """
        Create RiskType object and try to update its schema.
        """
        risk_type = self.create_risk_type()
        for r in risk_type.schema:
            if r['field_type'] == 'text':
                r['field_type'] = 'textarea'
                break

        response = self.client.put(
            f'/api/v0/risk-types/{risk_type.id}/',
            data={
                'type_name': 'New Risk Type',
                'schema': risk_type.schema,
            }, format='json')
        risk_type.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(risk_type.schema[0].get('field_type'), 'textarea')


class RiskTests(APITestCase):
    """
    Provide tests for Risk:
    1) creating Risk object;
    2) getting details of Risk object;
    3) updating Risk object for type_name;
    4) updating Risk object for schema param;
    """

    def create_risk_type(self):
        risk_type = RiskType.objects.create(
            type_name='New Risk Type',
            schema=TEST_SCHEMA
        )
        risk_type.save()

        return risk_type

    def create_risk(self):
        risk_type = self.create_risk_type()
        risk = Risk.objects.create(
            risk_type=risk_type,
            risk_data=TEST_RISK_DATA
        )
        risk.save()

        return risk

    def test_create_risk(self):
        """
        Ensure we can create a new Risk object in 2 steps:
        1) create RiskType object;
        2) create Risk object with relation to just created RiskType object.
        """
        risk_type_url = r'/api/v0/risk-types/'
        risk_type_data = {
            'type_name': 'New Risk Type',
            'schema': TEST_SCHEMA
        }
        response = self.client.post(
            risk_type_url, risk_type_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RiskType.objects.count(), 1)
        self.assertEqual(RiskType.objects.get().type_name, 'New Risk Type')

        risk_url = r'/api/v0/risk/'

        risk_type = RiskType.objects.get()
        risk_data = {
            'risk_type': risk_type.id,
            'risk_data': TEST_RISK_DATA
        }
        response = self.client.post(
            risk_url, risk_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Risk.objects.count(), 1)
        self.assertEqual(Risk.objects.get().risk_type.type_name,
                         'New Risk Type')

    def test_can_get_risk_details(self):
        """
        Creates Risk object and try to get it.
        """
        risk = self.create_risk()

        response = self.client.get(f'/api/v0/risk/{risk.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual((response.data['risk_type'],
                          response.data['risk_data']),
                         (RiskSerializer(instance=risk)['risk_type'].value,
                          RiskSerializer(instance=risk)['risk_data'].value))

    def test_can_update_risk_data(self):
        """
        Create Risk object and try to update its risk_data in 2 steps:
        1) create RiskType object and make updates to schema;
        2) create Risk object related to just created RiskType object and
        make updates to risk_data with new option.
        """
        faker = Faker()
        risk = self.create_risk()
        risk_type = RiskType.objects.get(id=risk.risk_type.id)
        new_first_name = faker.first_name()
        for r in risk.risk_data:
            if r['field_name'] == 'first_name':
                r['value'] = new_first_name
                break
        response = self.client.put(
            f'/api/v0/risk/{risk.id}/',
            data={
                'risk_type': risk_type.id,
                'risk_data': risk.risk_data
            }, format='json')
        risk.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(risk.risk_data[0].get('value'), new_first_name)
