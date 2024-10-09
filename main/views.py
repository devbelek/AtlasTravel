from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RestIdea, BestChoice, PopularHotel, RentOfCar, Benefits
from .serializers import RestIdeaSerializer, BestChoiceSerializer, PopularHotelSerializer, RentOfCarSerializer, BenefitsSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class HomePageView(APIView):
    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        rest_idea = RestIdea.objects.prefetch_related('tours__tags').first()
        best_choice = BestChoice.objects.prefetch_related('tours__tags').first()
        popular_hotel = PopularHotel.objects.prefetch_related('hotels__tags').first()

        rest_ideas_serializer = RestIdeaSerializer(rest_idea) if rest_idea else None
        best_choices_serializer = BestChoiceSerializer(best_choice) if best_choice else None
        popular_hotels_serializer = PopularHotelSerializer(popular_hotel) if popular_hotel else None

        response_data = {
            'rest_ideas': rest_ideas_serializer.data if rest_ideas_serializer else None,
            'best_choices': best_choices_serializer.data if best_choices_serializer else None,
            'popular_hotels': popular_hotels_serializer.data if popular_hotels_serializer else None,
        }

        return Response(response_data)


class RentOfCarViewSet(viewsets.ModelViewSet):
    queryset = RentOfCar.objects.prefetch_related('images', 'descriptions').all()
    serializer_class = RentOfCarSerializer

    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class BenefitsViewSet(viewsets.ModelViewSet):
    queryset = Benefits.objects.all()
    serializer_class = BenefitsSerializer

    @method_decorator(cache_page(60 * 60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
