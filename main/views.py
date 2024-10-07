from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RestIdea, BestChoice, PopularHotel, RentOfCar, Benefits
from .serializers import RestIdeaSerializer, BestChoiceSerializer, PopularHotelSerializer, RentOfCarSerializer, \
    BenefitsSerializer


class HomePageView(APIView):
    def get(self, request):
        rest_idea = RestIdea.objects.first()
        best_choice = BestChoice.objects.first()
        popular_hotel = PopularHotel.objects.first()

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
    queryset = RentOfCar.objects.all()
    serializer_class = RentOfCarSerializer


class BenefitsViewSet(viewsets.ModelViewSet):
    queryset = Benefits.objects.all()
    serializer_class = BenefitsSerializer
