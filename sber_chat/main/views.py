from django.shortcuts import render
from .models import ChatMessage
# from .utils import generate_response

def render_main_page(request):
    if request.method == "POST":
        query = request.POST.get("query")
        # response = generate_response(query)
        response = 'Окей'

        chat_message = ChatMessage.objects.create(query=query, response=response)

    messages = ChatMessage.objects.all()
    return render(request, 'main/main_page.html', {"messages": messages})
