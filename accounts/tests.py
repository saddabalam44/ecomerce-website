import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Address

CustomUser = get_user_model()

@pytest.mark.django_db
def test_custom_user_creation():
    user = CustomUser.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpassword123',
        phone_number='1234567890'
    )
    assert user.username == 'testuser'
    assert user.email == 'testuser@example.com'
    assert user.phone_number == '1234567890'
    assert user.is_email_verified is False
    assert user.is_staff is False
    assert str(user) == 'testuser@example.com'

@pytest.mark.django_db
def test_address_model_is_default_logic():
    user = CustomUser.objects.create_user(
        username='testuser2',
        email='testuser2@example.com',
        password='testpassword123'
    )
    
    addr1 = Address.objects.create(
        user=user,
        full_name="John Doe",
        address_line1="123 Main St",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        phone_number="9999999999",
        is_default=True
    )
    
    addr2 = Address.objects.create(
        user=user,
        full_name="John Doe 2",
        address_line1="456 Main St",
        city="Mumbai",
        state="Maharashtra",
        postal_code="400001",
        phone_number="9999999999",
        is_default=True
    )
    
    # Reload addr1
    addr1.refresh_from_db()
    assert addr1.is_default is False
    assert addr2.is_default is True
