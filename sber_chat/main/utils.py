from gigachat import GigaChat

class GigaChatAPI:
    def __init__(self, api_key):
        self.model = GigaChat(credentials=api_key, model="GigaChat", verify_ssl_certs=False)

    def send_message(self, query):
        messages = [{"role": "user", "content": query}]
        response = self.model.chat({"messages": messages})

        # Преобразуем в словарь перед использованием
        response_dict = response.dict()
        return response_dict["choices"][0]["message"]["content"]
