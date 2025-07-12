from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import datetime
from apps.projects.models import Project
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from apps.projects.serializers.project_serializers import (
    AllProjectsSerializer,
    CreateProjectSerializer,
    ProjectDetailSerializer,
)


class ProjectsListAPIView(APIView):

    def get_objects(self, date_from=None, date_to=None):
        projects = Project.objects.all()

        if date_from and date_to:
            try:
                date_from = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
                date_to = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d'))
                projects = projects.filter(created_at__range=[date_from, date_to])
            except ValueError:
                # Обработка случая, если дата передана в неправильном формате
                return Project.objects.none()

        return projects

    def get(self, request: Request) -> Response:
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        projects = self.get_objects(date_from, date_to)

        if not projects.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        serializer = AllProjectsSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CreateProjectSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    def get_object(self, pk: int):
        return get_object_or_404(Project, pk=pk)

    def get(self, request: Request, pk: int) -> Response:
        project = self.get_object(pk=pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk: int) -> Response:
        project = self.get_object(pk=pk)
        serializer = CreateProjectSerializer(
            instance=project,
            data=request.data,
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: int) -> Response:
        project = self.get_object(pk=pk)
        project.delete()
        return Response(data={"message": "Project was deleted successfully"},
                        status=status.HTTP_200_OK,
                        )
