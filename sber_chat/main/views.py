from django.shortcuts import render
from django.contrib import messages as django_messages
from .models import ChatMessage
import logging
from .utils import GigaChatAPI
from .contact_script import ContactSearch

# Настройка логирования
logger = logging.getLogger(__name__)



def render_main_page(request):
    if request.method == "POST":
        query = request.POST.get("query")
        if not query:
            django_messages.error(request, "Запрос не может быть пустым.")
            return render(request, 'main/main_page.html', {"messages": ChatMessage.objects.all()})

        # Путь к CSV-файлу
        csv_path = "/Users/isherz/Desktop/sber_chat/sber_chat/main/contacts.csv"
        contact_search = ContactSearch(csv_path)


        # Поиск в CSV
        csv_response = contact_search.query_contacts(query)

        if csv_response:
            response = csv_response
        else:
            # Если в CSV ничего не найдено, обращаемся к GigaChat API
            authorization_key = "Ваш_API_ключ"
            gigachat = GigaChatAPI(authorization_key)
            try:
                response = gigachat.send_message(query)
            except Exception as e:
                logger.error(f"Ошибка при взаимодействии с GigaChat API: {e}", exc_info=True)
                response = "Произошла ошибка при получении ответа. Попробуйте снова."

        # Сохраняем запрос и ответ в БД
        ChatMessage.objects.create(query=query, response=response)

    all_messages = ChatMessage.objects.all()
    return render(request, 'main/main_page.html', {"messages": all_messages})
