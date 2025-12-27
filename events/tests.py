from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Event, Photographer, Assignment

class AssignmentTests(APITestCase):
    def setUp(self):
        self.p1 = Photographer.objects.create(
            name="P1", email="p1@example.com", phone="111", is_active=True
        )
        self.p2 = Photographer.objects.create(
            name="P2", email="p2@example.com", phone="222", is_active=True
        )
        self.p3 = Photographer.objects.create(
            name="P3", email="p3@example.com", phone="333", is_active=True
        )
        self.p_inactive = Photographer.objects.create(
            name="P_Inactive", email="p_in@example.com", phone="000", is_active=False
        )

    def test_smart_assignment(self):
        future_date = date.today() + timedelta(days=10)
        event = Event.objects.create(
            event_name="Wedding",
            event_date=future_date,
            photographers_required=2
        )

        url = f'/api/events/{event.id}/assign-photographers/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['assigned_photographers']), 2)
        self.assertEqual(Assignment.objects.filter(event=event).count(), 2)

    def test_not_enough_photographers(self):
        future_date = date.today() + timedelta(days=12)
        event = Event.objects.create(
            event_name="Big Festival",
            event_date=future_date,
            photographers_required=10
        )

        url = f'/api/events/{event.id}/assign-photographers/'
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough available photographers', response.data['error'])

    def test_photographer_already_booked(self):
        future_date = date.today() + timedelta(days=15)
        
        event1 = Event.objects.create(
            event_name="Event 1",
            event_date=future_date,
            photographers_required=3
        )
        
        self.client.post(f'/api/events/{event1.id}/assign-photographers/')
        
        event2 = Event.objects.create(
            event_name="Event 2",
            event_date=future_date,
            photographers_required=1
        )
        
        response = self.client.post(f'/api/events/{event2.id}/assign-photographers/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # All 3 active are booked

    def test_assignment_logic_excludes_inactive(self):
         future_date = date.today() + timedelta(days=20)
         event = Event.objects.create(
            event_name="Gala",
            event_date=future_date,
            photographers_required=4
        )
         
         response = self.client.post(f'/api/events/{event.id}/assign-photographers/')
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         self.assertEqual(response.data['available'], 3)

    def test_past_event(self):
        past_date = date.today() - timedelta(days=1)
        event = Event.objects.create(
            event_name="Past Event",
            event_date=past_date,
            photographers_required=1
        )
        
        response = self.client.post(f'/api/events/{event.id}/assign-photographers/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('past', response.data['error'])

    def test_already_fulfilled_event(self):
        future_date = date.today() + timedelta(days=25)
        event = Event.objects.create(
            event_name="Double Book",
            event_date=future_date,
            photographers_required=1
        )
        

        self.client.post(f'/api/events/{event.id}/assign-photographers/')
        
        
        response = self.client.post(f'/api/events/{event.id}/assign-photographers/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already has assignments', response.data['error'])
