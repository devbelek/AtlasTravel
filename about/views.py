from .models import AboutUs
from .serializers import AboutUsSerializer
from rest_framework import viewsets


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer

