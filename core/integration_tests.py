import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_my_db():
    count = User.objects.filter().count()
    assert count == 0
