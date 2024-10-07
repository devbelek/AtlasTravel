from rest_framework import viewsets
from .models import Contacts
from .serializers import ContactstSerializer


class ContactsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactstSerializer
