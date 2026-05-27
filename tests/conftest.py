import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from projects.models import Project
from tasks.models import Task


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="test@test.com",
        name="Test User",
        password="testpass123",
    )


@pytest.fixture
def other_user(db):
    User = get_user_model()
    return User.objects.create_user(
        email="other@test.com",
        name="Other User",
        password="otherpass123",
    )


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def project(db, user):
    return Project.objects.create(
        name="Test Project", description="Test description", owner=user
    )


@pytest.fixture
def task(db, project, user):
    return Task.objects.create(
        title="Test Task",
        description="Test Description",
        project=project,
        assignee=user,
        priority="high",
    )
