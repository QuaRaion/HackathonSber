from django.shortcuts import render
from django.contrib import messages as django_messages
from .models import ChatMessage
import logging
from .utils import GigaChatAPI

# Настройка логирования
logger = logging.getLogger(__name__)

def render_main_page(request):
    if request.method == "POST":
        query = request.POST.get("query")

        if not query:
            django_messages.error(request, "Запрос не может быть пустым.")
            return render(request, 'main/main_page.html', {"messages": ChatMessage.objects.all()})

        authorization_key = "NmIyNTU4NzktMWU4OS00ZGY0LWIxYTItMmIxNDZjZjEwMzE4OjgyMjRmMmNjLTk2NzgtNDU4Mi1iZjZhLTI1NjNkNmMzYTJkZQ=="
        gigachat = GigaChatAPI(authorization_key)

        try:
            response = gigachat.send_message(query)
        except Exception as e:
            logger.error(f"Ошибка при взаимодействии с GigaChat API: {e}", exc_info=True)
            response = "Произошла ошибка при получении ответа. Попробуйте снова."

        ChatMessage.objects.create(query=query, response=response)

    all_messages = ChatMessage.objects.all()
    return render(request, 'main/main_page.html', {"messages": all_messages})
