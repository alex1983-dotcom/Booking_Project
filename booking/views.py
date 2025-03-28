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
        start = request.GET.get('start')  # Получаем время начала из параметров запроса
        end = request.GET.get('end')  # Получаем время окончания из параметров запроса

        if not start or not end:
            return Response({"error": "Параметры 'start' и 'end' обязательны."}, status=status.HTTP_400_BAD_REQUEST)

        # Исключаем пространства, которые заняты в указанный период
        available_spaces = Space.objects.exclude(
            booking__event_start_date__lt=end,
            booking__event_end_date__gt=start
        )

        serializer = SpaceSerializer(available_spaces, many=True)
        return Response({"spaces": serializer.data}, status=status.HTTP_200_OK)


class CreateBookingAPIView(APIView):
    """
    APIView для создания бронирования.
    """
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Получаем данные из запроса
            start = serializer.validated_data['event_start_date']
            end = serializer.validated_data['event_end_date']
            space = serializer.validated_data['space']

            # Проверка на пересечения с существующими бронированиями
            overlapping_bookings = Booking.objects.filter(
                space=space,
                event_start_date__lt=end,
                event_end_date__gt=start
            )

            if overlapping_bookings.exists():
                return Response({"error": "Время пересекается с существующими бронированиями."}, status=status.HTTP_400_BAD_REQUEST)

            # Сохраняем бронирование
            serializer.save()
            return Response({"status": "success", "booking": serializer.data}, status=status.HTTP_201_CREATED)

        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
