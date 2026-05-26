import pytest
from django.contrib.auth import get_user_model

from projects.models import Project
from tasks.models import Task


@pytest.mark.django_db
class TestUserModel:
    def test_create_user_with_email(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user@test.com",
            name="Test",
            password="pass123",
        )
        assert user.email == "user@test.com"
        assert user.check_password("pass123")

    def test_create_user_without_email_raises_error(self):
        User = get_user_model()
        with pytest.raises(ValueError, match="El email es obligatorio"):
            User.objects.create_user(
                email="",
                name="Test",
                password="pass123",
            )

    def test_create_superuser(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            email="admin@test.com",
            name="Admin",
            password="admin123",
        )
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_user_str(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user@test.com",
            name="Test",
            password="pass123",
        )
        assert str(user) == "user@test.com"


@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self, user):
        project = Project.objects.create(
            name="Test Project",
            owner=user,
        )
        assert project.name == "Test Project"
        assert project.status == Project.Status.ACTIVE

    def test_project_str(self, user):
        project = Project.objects.create(name="My Project", owner=user)
        assert str(project) == "My Project"

    def test_project_default_status(self, user):
        project = Project.objects.create(name="Test", owner=user)
        assert project.status == Project.Status.ACTIVE


@pytest.mark.django_db
class TestTaskModel:
    def test_create_task(self, project, user):
        task = Task.objects.create(
            title="Test Task",
            project=project,
            assignee=user,
        )
        assert task.title == "Test Task"
        assert task.status == Task.Status.PENDING
        assert task.priority == Task.Priority.MEDIUM

    def test_task_str(self, project):
        task = Task.objects.create(title="My Task", project=project)
        assert str(task) == "My Task"

    def test_task_without_assignee(self, project):
        task = Task.objects.create(title="Unassigned", project=project)
        assert task.assignee is None
