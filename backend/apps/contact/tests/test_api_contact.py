import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.contact.models import Contact, Label

@pytest.fixture()
def client():
    return APIClient()

@pytest.fixture()
def labels():
    return [
        Label.objects.create(name="label1"),
        Label.objects.create(name="label2"),
        Label.objects.create(name="label3"),
    ]

@pytest.fixture()
def make_contact():
    def _make(name, profile_url=None, email=None, phone=None, company=None, labels=None):
        c = Contact.objects.create(
            profile_url=profile_url,
            name=name,
            email=email,
            phone=phone,
            company=company,
        )
        if labels:
            c.labels.set(labels)
        return c
    return _make

@pytest.mark.django_db
def test_contact_list_ok(client, make_contact):
    make_contact("test", email="a@test.com", phone="1234567890", company="company")
    make_contact("test2", email="b@test.com", phone="0987654321", company="company2")
    
    response = client.get(reverse('contact-list'))

    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]['name'] == "test"
    assert response.data["results"][1]['name'] == "test2"
    
@pytest.mark.django_db
def test_contact_detail_ok(client, make_contact):
    contact = make_contact("test", email="a@test.com", phone="1234567890", company="company")
    
    response = client.get(reverse('contact-detail', kwargs={'pk': contact.id}))
    assert response.status_code == 200
    assert response.data['name'] == "test"
    assert response.data['email'] == "a@test.com"
    assert response.data['phone'] == "1234567890"
    assert response.data['company'] == "company"
    
@pytest.mark.django_db
def test_contact_create_ok(client, labels):
    label1 = labels[0]
    label2 = labels[1]
    
    data = {
        "name": "test",
        "email": "test@test.com",
        "phone": "1234567890",
        "company": "test_company",
        "labels": [label1.id, label2.id]
    }
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == data.get('name')
    assert response.data['email'] == data.get('email')
    assert response.data['phone'] == data.get('phone')
    assert response.data['company'] == data.get('company')
    assert len(response.data['labels']) == 2
    
@pytest.mark.django_db
def test_contact_create_invalid_email(client):
    data = {
        "name": "test",
        "email": "invalid-email",
        "phone": "1234567890",
        "company": "test_company"
    }
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 400
    assert 'email' in response.data
    assert response.data['email'][0] == "유효한 이메일 주소를 입력하세요."
    
@pytest.mark.django_db
def test_contact_create_invalid_phone(client):
    data = {
        "name": "test",
        "phone": "invalid-phone",
    }
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 400
    assert 'phone' in response.data
    assert response.data['phone'][0] == "전화번호는 숫자, +, -만 포함할 수 있습니다."

@pytest.mark.django_db
def test_contact_create_phone_ok(client):
    data = {
        "name": "test",
        "phone": "+8210-1234-5678",
    }

    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 201
    assert response.data['phone'] == data.get('phone')
    
@pytest.mark.django_db
def test_contact_create_phone_length(client):
    data = {
        "name": "test",
        "phone": "1234567890123456",  # 16 characters
    }
    
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 400
    assert 'phone' in response.data
    assert response.data['phone'][0] == "전화번호는 최대 15자리 이하이어야 합니다."
    
@pytest.mark.django_db
def test_contact_create_profile_url(client):
    data = {
        "name": "test",
        "profile_url": "example.com/profile.jpg"
    }
    
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 400
    assert 'profile_url' in response.data
    assert response.data['profile_url'][0] == "유효한 URL을 입력하세요."
    
@pytest.mark.django_db
def test_contact_create_profile_url_ok(client):
    data = {
        "name": "test",
        "profile_url": "http://example.com/profile.jpg"
    }
    
    response = client.post(reverse('contact-list'), data, format='json')
    assert response.status_code == 201
    assert response.data['profile_url'] == data.get('profile_url')

@pytest.mark.django_db
def test_contact_label_ok(client):
    data = {
        "name": "test",
    }
    
    response = client.post(reverse('contact-label-list'), data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == data.get('name')
    
@pytest.mark.django_db
def test_contact_list_orderby_ok(client, make_contact):   
    make_contact("test1", email="a@test.com", phone="1234567890", company="company1")
    make_contact("test2", email="b@test.com", phone="0987654321", company="company2")
    make_contact("test3", email="c@test.com", phone="1122334455", company="company3")
    
    response = client.get(reverse('contact-list'), {'ordering': 'name'})
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]['name'] == "test1"
    assert response.data["results"][2]['name'] == "test3"
    
    response = client.get(reverse('contact-list'), {'ordering': '-email'})
    assert response.status_code == 200
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]['email'] == "c@test.com"
    assert response.data["results"][2]['email'] == "a@test.com"