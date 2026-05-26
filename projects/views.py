from rest_framework import viewsets

from projects.models import Project
from projects.permissions import IsOwnerOrReadOnly
from projects.serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Project.objects.none()
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
