import pytest
from rest_framework import status

from projects.models import Project
from tasks.models import Task


@pytest.mark.django_db
class TestAuthAPI:
    def test_register_user(self, api_client):
        response = api_client.post(
            "/api/v1/users/register/",
            {
                "email": "new@test.com",
                "name": "New User",
                "password": "newpass123",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "id" in response.data
        assert response.data["email"] == "new@test.com"

    def test_login_get_token(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/token/",
            {
                "email": "test@test.com",
                "password": "testpass123",
            },
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_login_wrong_password(self, api_client, user):
        response = api_client.post(
            "/api/v1/auth/token/",
            {
                "email": "test@test.com",
                "password": "wrongpass",
            },
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestProjectAPI:
    def test_create_project(self, auth_client):
        response = auth_client.post(
            "/api/v1/projects/",
            {
                "name": "New Project",
                "description": "Description",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["name"] == "New Project"

    def test_list_projects(self, auth_client, project):
        response = auth_client.get("/api/v1/projects/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_cannot_see_other_user_projects(self, auth_client, other_user):
        Project.objects.create(name="Other Project", owner=other_user)
        response = auth_client.get("/api/v1/projects/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

    def test_unauthenticated_cannot_access(self, api_client):
        response = api_client.get("/api/v1/projects/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTaskAPI:
    def test_create_task(self, auth_client, project):
        response = auth_client.post(
            "/api/v1/tasks/",
            {
                "title": "New Task",
                "project": project.id,
                "priority": "high",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["title"] == "New Task"

    def test_list_tasks(self, auth_client, task):
        response = auth_client.get("/api/v1/tasks/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_filter_tasks_by_status(self, auth_client, project):
        Task.objects.create(
            title="Pending", project=project, status=Task.Status.PENDING
        )
        Task.objects.create(
            title="Completed", project=project, status=Task.Status.COMPLETED
        )
        response = auth_client.get("/api/v1/tasks/", {"status": "pending"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1

    def test_search_tasks(self, auth_client, project):
        Task.objects.create(title="Backend API", project=project)
        Task.objects.create(title="Frontend UI", project=project)
        response = auth_client.get("/api/v1/tasks/", {"search": "Backend"})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
