from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Person
from .serializers import PersonSerializer


class PersonViewSet(viewsets.ViewSet):
    def list(self, request):
        """GET /api/v1/persons/ - Получение всех записей"""
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET /api/v1/persons/{id} - Получение записи по ID"""
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def create(self, request):
        """POST /api/v1/persons/ - Создание новой записи"""
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            person = serializer.save()
            location = f'/api/v1/persons/{person.id}'
            return Response(status=status.HTTP_201_CREATED, headers={'Location': location})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        """PATCH /api/v1/persons/{id} - Обновление записи"""
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(person, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """DELETE /api/v1/persons/{id} - Удаление записи"""
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
