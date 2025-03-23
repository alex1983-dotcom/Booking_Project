from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Space, Equipment, Booking, Parking
from .serializers import SpaceSerializer, BookingSerializer, EquipmentSerializer, ParkingSerializer

class SpaceListView(APIView):
    """
    Получение списка залов
    """
    def get(self, request):
        try:
            spaces = Space.objects.all()
            if not spaces:
                return Response({"message": "Нет доступных залов."}, status=status.HTTP_404_NOT_FOUND)
            serializer = SpaceSerializer(spaces, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.permissions import IsAuthenticatedOrReadOnly

class BookingCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Бронирование успешно создано!"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        return Response({"message": "Метод GET не поддерживается для создания бронирований."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class EquipmentListView(APIView):
    """
    Получение списка оборудования
    """
    def get(self, request):
        try:
            space_id = request.query_params.get('space_id')
            if space_id:
                equipments = Equipment.objects.filter(space_id=space_id)
            else:
                equipments = Equipment.objects.all()
            if not equipments:
                return Response({"message": "Оборудование отсутствует."}, status=status.HTTP_404_NOT_FOUND)
            serializer = EquipmentSerializer(equipments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ParkingListView(APIView):
    """
    Получение списка парковок
    """
    def get(self, request):
        try:
            parkings = Parking.objects.all()
            if not parkings:
                return Response({"message": "Нет доступных парковок."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ParkingSerializer(parkings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.generics import RetrieveAPIView
from .models import Space
from .serializers import SpaceSerializer

class SpaceDetailView(RetrieveAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer

from rest_framework.generics import ListAPIView
from .models import Booking
from .serializers import BookingSerializer

class BookingListView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
