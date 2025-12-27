from django.urls import path

from .views import (
    assign_photographers,
    event_assignments,
    event_detail,
    event_list_create,
    photographer_detail,
    photographer_list_create,
    photographer_schedule,
)

urlpatterns = [
    path('events/', event_list_create),
    path('events/<int:pk>/', event_detail),
    path('events/<int:id>/assign-photographers/', assign_photographers),
    path('events/<int:id>/assignments/', event_assignments),
    path('photographers/', photographer_list_create),
    path('photographers/<int:pk>/', photographer_detail),
    path('photographers/<int:id>/schedule/', photographer_schedule),
]
