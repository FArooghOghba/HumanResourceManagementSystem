from rest_framework import status
from rest_framework.reverse import reverse


EMPLOYEE_CREATE_URL = reverse('employees:create')


def test_create_employee_success(
        api_client, first_test_employee_payload
) -> None:

    response = api_client.post(path=EMPLOYEE_CREATE_URL, data=first_test_employee_payload)

    assert response.status_code == status.HTTP_201_CREATED
    assert 'id' in response.data


# def test_create_employee_duplicate_phone(api_client, employee_factory):
#     existing = employee_factory.create(phone="+1234567890")
#
#     response = api_client.post('/api/employees/', {
#         # ... same data as above with existing phone
#     }, format='json')
#
#     assert response.status_code == 400
#     assert "Phone number already registered" in str(response.data)