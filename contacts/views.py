from rest_framework import viewsets
from rest_framework.response import Response

from .models import Contacts
from .serializers import ContactsSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class ContactsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    def get_object(self):
        return self.queryset.first()

    @method_decorator(cache_page(60 * 60))
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
