from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Space, Booking
from .serializers import SpaceSerializer, BookingSerializer

class CheckAvailabilityAPIView(APIView):
    """
    APIView для проверки доступности пространств.
    """
    def get(self, request):
        available_spaces = Space.objects.filter(available=True)
        serializer = SpaceSerializer(available_spaces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateBookingAPIView(APIView):
    """
    APIView для создания бронирования.
    """
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
