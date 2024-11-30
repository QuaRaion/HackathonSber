import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Загрузка модели и токенизатора
tokenizer = AutoTokenizer.from_pretrained("ai-forever/ruGPT-3.5-13B")
model = AutoModelForCausalLM.from_pretrained("ai-forever/ruGPT-3.5-13B")

# Создаем pipeline для генерации текста
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)


# Загрузка базы данных телефонов из Excel
def load_phone_data(file_path):
    data = pd.read_excel(file_path)
    # Преобразуем данные в список словарей
    return data.to_dict(orient="records")


# Функция поиска номера телефона
def search_phone(phone_number, phones):
    for phone in phones:
        if phone["phones"] == phone_number:
            category = phone.get("category", "Категория не указана.")
            name = phone.get("name", "Название не указано.")
            add_phone = phone.get("add_phone", "Дополнительная информация отсутствует.")
            return (f"Номер {phone_number} найден в базе.\n"
                    f"Категория: {category}\n"
                    f"Название: {name}\n"
                    f"Дополнительная информация: {add_phone}")
    return f"Номер {phone_number} не найден в базе."


# Функция для генерации ответа с использованием модели ruGPT-3.5-13B
def ask_gpt3_5(prompt):
    # Генерация текста с моделью
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']


# Основная функция взаимодействия
def main():
    # Загрузка данных из Excel
    phones = load_phone_data("phones.xlsx")

    print("Добро пожаловать! Вы можете искать номера телефонов в базе.")
    while True:
        user_input = input("Введите номер телефона (или 'выход' для завершения): ")
        if user_input.lower() == "выход":
            print("До свидания!")
            break

        # Проверяем номер в базе
        result = search_phone(user_input, phones)
        print(result)

        # Формируем запрос для модели ruGPT-3.5
        prompt = f"Найди номер {user_input} в базе данных и предоставь информацию по категории, названию и дополнительной информации. Если номер не найден, напиши, что его нет в базе."

        # Получаем ответ от модели
        gpt3_response = ask_gpt3_5(prompt)
        print(f"Ответ от модели ruGPT-3.5-13B: {gpt3_response}")


if __name__ == "__main__":
    main()
