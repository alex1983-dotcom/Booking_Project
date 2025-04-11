from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from .models import Space, Booking, AdditionalPreference, Feedback
from .serializers import SpaceSerializer, BookingSerializer, PreferenceSerializer, FeedbackSerializer
from datetime import datetime
from django.utils.timezone import make_aware
import logging

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


# === Эндпоинты для управления пространствами ===

class CheckAvailabilityAPIView(APIView):
    """
    Проверяет доступность пространств.
    """
    def get(self, request):
        try:
            start = request.GET.get('start')
            end = request.GET.get('end')
            guests = request.GET.get('guests')

            logger.info(f"Полученные параметры: start={start}, end={end}, guests={guests}")

            if not start or not end:
                return create_error_response("Параметры 'start' и 'end' обязательны.")

            start_date = validate_date(start)
            end_date = validate_date(end)

            if start_date >= end_date:
                return create_error_response("Дата начала должна быть раньше даты окончания.")

            # Удаляем фильтр по вместимости залов (capacity__gte)
            available_spaces = Space.objects.exclude(
                booking__event_start_date__lt=end_date,
                booking__event_end_date__gt=start_date
            ).distinct()

            logger.info(f"Найдено {available_spaces.count()} доступных пространств.")
            serializer = SpaceSerializer(available_spaces, many=True)
            return create_success_response({"spaces": serializer.data})
        except serializers.ValidationError as ve:
            logger.error(f"Ошибка валидации: {ve}")
            return create_error_response("Неверный формат даты. Используйте формат 'YYYY-MM-DD HH:MM'.")
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)



# === Эндпоинты для управления бронированием ===

class CreateBookingAPIView(APIView):
    """
    Создаёт бронирование с привязкой к контактам пользователя.
    """
    def post(self, request):
        try:
            logger.info(f"Полученные данные: {request.data}")

            # Преобразование мессенджера
            messenger_mapping = {
                "viber": Feedback.Messenger.VIBER,
                "telegram": Feedback.Messenger.TELEGRAM,
                "whatsapp": Feedback.Messenger.WHATSAPP
            }

            messenger_value = messenger_mapping.get(
                request.data.get("messenger", "viber").lower(),  # По умолчанию "viber"
                Feedback.Messenger.VIBER
            )
            request.data["messengers"] = messenger_value

            # Создание контакта (Feedback)
            feedback_data = {
                "name": request.data.get("client_name"),
                "phone_number": request.data.get("client_contact"),
                "email": request.data.get("email"),
                "promo_code": request.data.get("promo_code"),
                "messengers": request.data.get("messengers")
            }

            feedback_serializer = FeedbackSerializer(data=feedback_data)
            if feedback_serializer.is_valid():
                feedback_instance = feedback_serializer.save()
                logger.info(f"Контакт создан: {feedback_instance.id}")
            else:
                logger.warning(f"Ошибка в данных контакта: {feedback_serializer.errors}")
                return create_error_response(feedback_serializer.errors, status.HTTP_400_BAD_REQUEST)

            # Создание бронирования (Booking)
            booking_serializer = BookingSerializer(data=request.data)
            if booking_serializer.is_valid():
                booking = booking_serializer.save(contact=feedback_instance)  # Привязка контакта к бронированию
                logger.info(f"Бронирование создано: {booking.id}")
                return create_success_response({"booking": booking_serializer.data}, status.HTTP_201_CREATED)
            else:
                logger.warning(f"Ошибка в данных бронирования: {booking_serializer.errors}")
                return create_error_response(booking_serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Ошибка при создании бронирования: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)


# === Эндпоинты для управления предпочтениями ===

class PreferencesAPIView(APIView):
    """
    API для получения и обработки предпочтений.
    """
    def get(self, request):
        try:
            preferences = AdditionalPreference.objects.all()
            serializer = PreferenceSerializer(preferences, many=True)
            logger.info(f"Возвращаем {len(serializer.data)} предпочтений.")
            return create_success_response({"preferences": serializer.data})
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            preference_data = request.data.get("preferences", [])
            if not preference_data:
                return create_error_response("Данные предпочтений отсутствуют.", status.HTTP_400_BAD_REQUEST)

            logger.info(f"Полученные предпочтения: {preference_data}")

            processed_preferences = []
            for pref in preference_data:
                preference, created = AdditionalPreference.objects.get_or_create(
                    id=pref["id"], defaults={"name": pref["name"]}
                )
                if not created:
                    preference.name = pref["name"]
                    preference.save()
                processed_preferences.append({"id": preference.id, "name": preference.name})

            return create_success_response({"processed_preferences": processed_preferences})
        except Exception as e:
            logger.error(f"Ошибка при обработке предпочтений: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)


# === Эндпоинты для обратной связи ===

class FeedbackAPIView(APIView):
    """
    Обрабатывает обратную связь от клиентов.
    """
    def get(self, request):
        try:
            feedbacks = Feedback.objects.all()
            serializer = FeedbackSerializer(feedbacks, many=True)
            logger.info(f"Найдено отзывов: {len(serializer.data)}")
            return create_success_response({"feedbacks": serializer.data})
        except Exception as e:
            logger.error(f"Ошибка сервера: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = FeedbackSerializer(data=request.data)
            if serializer.is_valid():
                feedback = serializer.save()
                logger.info(f"Отзыв успешно сохранён: {feedback.id}")
                return create_success_response({"feedback": serializer.data}, status.HTTP_201_CREATED)

            logger.warning(f"Ошибка в данных: {serializer.errors}")
            return create_error_response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Ошибка при сохранении отзыва: {str(e)}")
            return create_error_response(f"Ошибка сервера: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
