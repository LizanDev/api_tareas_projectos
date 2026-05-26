from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = Project
        fields = ("id", "name", "description", "owner", "status", "created_at", "updated_at")
        read_only_fields = ("owner", "created_at", "updated_at")