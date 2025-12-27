from datetime import date

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Assignment, Event, Photographer
from .serializers import (
    AssignmentSerializer,
    EventSerializer,
    PhotographerSerializer,
)


@api_view(['GET', 'POST'])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all().order_by('-created_at')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def assign_photographers(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'},
            status=status.HTTP_404_NOT_FOUND,
        )
    if event.photographers_required <= 0:
        return Response(
            {'error': 'Photographers required must be greater than 0'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if event.event_date < date.today():
        return Response(
            {'error': 'Cannot assign photographers to past events'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    current_assignments_count = Assignment.objects.filter(event=event).count()
    if current_assignments_count > 0:
        return Response(
            {'error': 'Event already has assignments'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    required_count = event.photographers_required
    active_photographers = Photographer.objects.filter(is_active=True)

    booked_photographer_ids = Assignment.objects.filter(
        event__event_date=event.event_date
    ).values_list('photographer_id', flat=True)

    available_photographers = active_photographers.exclude(
        id__in=booked_photographer_ids
    )

    if available_photographers.count() < required_count:
        return Response(
            {
                'error': 'Not enough available photographers',
                'required': required_count,
                'available': available_photographers.count(),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    photographers_to_assign = available_photographers[:required_count]
    assignments = []
    
    with transaction.atomic():
        for photographer in photographers_to_assign:
            assignments.append(
                Assignment(event=event, photographer=photographer)
            )
        Assignment.objects.bulk_create(assignments)

    assigned_photographers_serializer = PhotographerSerializer(
        photographers_to_assign, many=True
    )
    
    return Response(
        {
            'message': 'Photographers assigned successfully',
            'assigned_photographers': assigned_photographers_serializer.data,
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET', 'POST'])
def photographer_list_create(request):
    if request.method == 'GET':
        photographers = Photographer.objects.all()
        serializer = PhotographerSerializer(photographers, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PhotographerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(['GET', 'PUT', 'DELETE'])
def photographer_detail(request, pk):
    try:
        photographer = Photographer.objects.get(pk=pk)
    except Photographer.DoesNotExist:
        return Response(
            {'error': 'Photographer not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == 'GET':
        serializer = PhotographerSerializer(photographer)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PhotographerSerializer(
            photographer,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == 'DELETE':
        photographer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def photographer_schedule(request, id):
    try:
        photographer = Photographer.objects.get(pk=id)
    except Photographer.DoesNotExist:
        return Response(
            {'error': 'Photographer not found'},
            status=status.HTTP_404_NOT_FOUND,
        )

    assignments = Assignment.objects.filter(
        photographer=photographer
    ).select_related('event')
    
    events = [a.event for a in assignments]
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def event_assignments(request, id):
    assignments = Assignment.objects.filter(
        event_id=id
    ).select_related('photographer')

    serializer = AssignmentSerializer(assignments, many=True)
    return Response(serializer.data)
