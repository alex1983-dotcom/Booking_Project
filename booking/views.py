from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Space, Booking, AdditionalPreference
from .serializers import SpaceSerializer, BookingSerializer, PreferenceSerializer
from datetime import datetime
from django.utils.timezone import make_aware

class CheckAvailabilityAPIView(APIView):
    """
    APIView для проверки доступности пространств.
    """
    def get(self, request):
        # Получение параметров из запроса
        start = request.GET.get('start')
        end = request.GET.get('end')
        guests = request.GET.get('guests')

        # Проверка наличия обязательных параметров
        if not start or not end or not guests:
            return Response(
                {"error": "Параметры 'start', 'end' и 'guests' обязательны."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Парсим дату и добавляем информацию о временной зоне
            start_date = make_aware(datetime.strptime(start, "%Y-%m-%d %H:%M"))
            end_date = make_aware(datetime.strptime(end, "%Y-%m-%d %H:%M"))

            if start_date >= end_date:
                return Response(
                    {"error": "Дата начала должна быть раньше даты окончания."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Проверка количества гостей
            try:
                guests_count = int(guests)
                if guests_count <= 0:
                    return Response(
                        {"error": "Количество гостей должно быть положительным числом."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            except ValueError:
                return Response(
                    {"error": "Некорректное значение параметра 'guests'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Фильтрация доступных пространств
            available_spaces = Space.objects.filter(
                capacity__gte=guests_count
            ).exclude(
                booking__event_start_date__lt=end_date,
                booking__event_end_date__gt=start_date
            )

            # Сериализация результатов
            serializer = SpaceSerializer(available_spaces, many=True)
            return Response({"spaces": serializer.data}, status=status.HTTP_200_OK)

        except ValueError:
            return Response(
                {"error": "Неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Ошибка на сервере: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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

            try:
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

            except Exception as e:
                return Response({"error": f"Ошибка сервера: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetPreferencesAPIView(APIView):
    """
    APIView для получения доступных дополнительных предпочтений.
    """
    def get(self, request):
        try:
            # Получаем все доступные предпочтения
            preferences = AdditionalPreference.objects.all()
            serializer = PreferenceSerializer(preferences, many=True)
            return Response({"preferences": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Ошибка сервера: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
