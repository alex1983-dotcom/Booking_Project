from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Space, Booking, AdditionalPreference, Feedback
from .serializers import SpaceSerializer, BookingSerializer, PreferenceSerializer, FeedbackSerializer
from datetime import datetime
from django.utils.timezone import make_aware
import logging
from rest_framework import serializers

logger = logging.getLogger(__name__)

# === Вспомогательные методы ===
def create_error_response(message: str, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Создаёт объект ошибки для ответа API.
    """
    return Response({"status": "error", "message": message}, status=status_code)

def create_success_response(data: dict, status_code=status.HTTP_200_OK):
    """
    Создаёт успешный объект ответа API.
    """
    return Response({"status": "success", "data": data}, status=status_code)

def validate_date(date_str: str):
    """
    Проверяет и преобразует дату в объект datetime.
    """
    try:
        return make_aware(datetime.strptime(date_str, "%Y-%m-%d %H:%M"))
    except ValueError:
        raise serializers.ValidationError(f"Некорректная дата: {date_str}")

# === Проверка доступности пространств ===
class CheckAvailabilityAPIView(APIView):
    """
    Проверяет доступность пространств.
    """
    def get(self, request):
        try:
            # Извлечение параметров из запроса
            start = request.GET.get('start')
            end = request.GET.get('end')
            guests = request.GET.get('guests')

            logger.info(f"Полученные параметры: start={start}, end={end}, guests={guests}")

            # Проверка наличия обязательных параметров
            if not start or not end or not guests:
                logger.warning("Отсутствуют обязательные параметры: 'start', 'end' или 'guests'.")
                return create_error_response("Параметры 'start', 'end' и 'guests' обязательны.", status.HTTP_400_BAD_REQUEST)

            # Валидация форматов дат
            start_date = validate_date(start)
            logger.info(f"Начальная дата прошла валидацию: {start_date}")
            end_date = validate_date(end)
            logger.info(f"Конечная дата прошла валидацию: {end_date}")

            if start_date >= end_date:
                logger.warning("Дата начала должна быть раньше даты окончания.")
                return create_error_response("Дата начала должна быть раньше даты окончания.", status.HTTP_400_BAD_REQUEST)

            # Проверка количества гостей
            guests_count = int(guests)
            if guests_count <= 0:
                logger.warning("Количество гостей должно быть положительным числом.")
                return create_error_response("Количество гостей должно быть положительным числом.", status.HTTP_400_BAD_REQUEST)

            # Поиск доступных пространств
            available_spaces = Space.objects.filter(
                capacity__gte=guests_count
            ).exclude(
                booking__event_start_date__lt=end_date,
                booking__event_end_date__gt=start_date
            )
            logger.info(f"Найдено {available_spaces.count()} доступных пространств.")

            # Сериализация данных
            serializer = SpaceSerializer(available_spaces, many=True)
            logger.info(f"Сериализация прошла успешно. Возвращаем данные.")
            return create_success_response({"spaces": serializer.data})

        except serializers.ValidationError as ve:
            logger.error(f"Ошибка валидации: {ve}")
            return create_error_response("Неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM'.", status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            logger.error(f"Ошибка при преобразовании числа: {ve}")
            return create_error_response("Ошибка в параметрах запроса. Проверьте данные.", status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Внутренняя ошибка сервера: {e}")
            return create_error_response(f"Ошибка сервера: {e}", status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateBookingAPIView(APIView):
    def post(self, request):
        logger.info(f"Полученные данные: {request.data}")
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            start = serializer.validated_data['event_start_date']
            end = serializer.validated_data['event_end_date']
            space = serializer.validated_data['space']

            try:
                overlapping_bookings = Booking.objects.filter(
                    space=space,
                    event_start_date__lt=end,
                    event_end_date__gt=start
                )
                if overlapping_bookings.exists():
                    return create_error_response("Время пересекается с существующими бронированиями.")

                serializer.save()
                return create_success_response({"status": "success", "booking": serializer.data}, status.HTTP_201_CREATED)

            except Exception as e:
                logger.error(f"Ошибка при сохранении бронирования: {str(e)}")
                return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning(f"Ошибка в данных: {serializer.errors}")
        return create_error_response(serializer.errors)


# === Получение предпочтений ===
class GetPreferencesAPIView(APIView):
    """
    Получает список доступных предпочтений.
    """
    def get(self, request):
        try:
            preferences = AdditionalPreference.objects.all()
            serializer = PreferenceSerializer(preferences, many=True)
            return create_success_response({"preferences": serializer.data})
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)


# === Обратная связь ===
class FeedbackAPIView(APIView):
    """
    Обрабатывает обратную связь от клиентов.
    """
    def get(self, request):
        """
        Получение списка всех контактов.
        """
        try:
            feedbacks = Feedback.objects.all()
            serializer = FeedbackSerializer(feedbacks, many=True)
            return create_success_response({"feedbacks": serializer.data})
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Создание нового контакта.
        """
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return create_success_response({"status": "success", "feedback": serializer.data}, status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Ошибка сервера: {str(e)}")
                return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.warning(f"Ошибка в данных: {serializer.errors}")
        return create_error_response(serializer.errors)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AdditionalPreference
from .serializers import PreferenceSerializer
import logging

logger = logging.getLogger(__name__)

class PreferencesAPIView(APIView):
    """
    API для получения и обработки предпочтений.
    """

    def get(self, request):
        """
        Возвращает список всех доступных предпочтений.
        """
        try:
            preferences = AdditionalPreference.objects.all()
            serializer = PreferenceSerializer(preferences, many=True)
            return Response({"preferences": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return Response({"error": f"Ошибка сервера: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Принимает данные предпочтений от клиента (бота).
        """
        try:
            preference_data = request.data.get("preferences", [])
            if not preference_data:
                return Response(
                    {"error": "Данные предпочтений отсутствуют."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Логируем полученные данные
            logger.info(f"Полученные предпочтения: {preference_data}")

            # Проверяем формат данных
            for pref in preference_data:
                if not isinstance(pref, dict) or "id" not in pref or "name" not in pref:
                    return Response(
                        {"error": f"Неверный формат данных предпочтения: {pref}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Обработка данных предпочтений
            processed_preferences = []
            for pref in preference_data:
                pref_id = pref["id"]
                pref_name = pref["name"]

                # Проверяем существование предпочтения в базе
                preference, created = AdditionalPreference.objects.get_or_create(
                    id=pref_id, defaults={"name": pref_name}
                )
                if not created:
                    preference.name = pref_name  # Обновляем название, если предпочтение уже существует
                    preference.save()
                
                processed_preferences.append({"id": preference.id, "name": preference.name})

            return Response(
                {"status": "success", "processed_preferences": processed_preferences},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Ошибка при обработке предпочтений: {str(e)}")
            return Response(
                {"error": f"Ошибка сервера: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

