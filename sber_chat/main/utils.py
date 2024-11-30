from gigachat import GigaChat

class GigaChatAPI:
    def __init__(self, api_key):
        self.model = GigaChat(credentials=api_key, model="GigaChat", verify_ssl_certs=False)

    def send_message(self, query):
        messages = [{"role": "user", "content": query}]
        response = self.model.chat({"messages": messages})

        response_dict = response.dict()
        return response_dict["choices"][0]["message"]["content"]

    def choose_best_option(self, query, options_list):
        """
        Выбирает наиболее подходящий вариант из списка на основе запроса.
        :param query: Пользовательский запрос
        :param options_list: Список словарей с вариантами
        :return: Текстовый ответ от GigaChat с наиболее подходящим вариантом
        """
        options_text = "\n".join(
            [f"{i + 1}. {option}" for i, option in enumerate(options_list)]
        )
        prompt = (
            f"У меня есть список возможных вариантов:\n{options_text}\n\n"
            f"Заполни шаблон с наиболее похожим на запрос пользователя вариантом (если есть несколько похожих подставляй любой): '{query}'? "
            f"1 шаблон (если нашло): Вы можете позвонить name по phones"
            f"2 шаблон (если похожих нет): Не могу найти"
            f"В ответе напиши только шаблон с подставленными данными из объекта и больше ничего"
        )

        messages = [{"role": "user", "content": prompt}]
        try:
            response = self.model.chat({"messages": messages})
            response_dict = response.dict()
            return response_dict["choices"][0]["message"]["content"]
        except Exception as e:
            raise Exception(f"Ошибка при выборе лучшего варианта: {e}")
