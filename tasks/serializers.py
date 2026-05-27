from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    assignee_email = serializers.ReadOnlyField(source="assignee.email")
    project_name = serializers.ReadOnlyField(source="project.name")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "project",
            "project_name",
            "assignee",
            "assignee_email",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "assignee_email",
            "project_name",
            "created_at",
            "updated_at",
        )
