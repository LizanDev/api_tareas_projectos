from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from tasks.models import Task
from tasks.permissions import IsProjectOwnerOrReadOnly
from tasks.serializers import TaskSerializer

# Create your views here.

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsProjectOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "priority", "project", "assignee"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "due_date", "priority"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return Task.objects.filter(project__owner=self.request.user)
    
    