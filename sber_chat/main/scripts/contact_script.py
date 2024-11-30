import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
class ContactSearch:
    def __init__(self, file_path, model_name='paraphrase-MiniLM-L6-v2'):
        # Инициализация модели и пути к файлу
        self.model = SentenceTransformer(model_name)
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        # Загрузка данных из CSV
        return pd.read_csv(self.file_path)

    def create_embeddings(self):
        # Векторизация текста
        self.data['text'] = self.data.apply(lambda x: f"{x['category']} {x['name']}", axis=1)
        self.data['embedding'] = self.data['text'].apply(lambda x: self.model.encode(x))

    def search(self, query, top_k=3):
        # Векторизация запроса
        query_vec = self.model.encode(query)

        # Расчет косинусного сходства
        self.data['similarity'] = self.data['embedding'].apply(lambda x: np.dot(query_vec, x) /
                                                                (np.linalg.norm(query_vec) * np.linalg.norm(x)))

        # Сортировка по релевантности и выбор топовых результатов
        results = self.data.sort_values(by='similarity', ascending=False).head(top_k)
        return results[['id', 'name', 'category', 'phones', 'add_phone']]

    def generate_response(self, results):
        # Генерация ответа на основе результатов
        if results.empty:
            return "Извините, информация по вашему запросу не найдена."

        response = "Вот что удалось найти:\n"
        for _, row in results.iterrows():
            response += f"- {row['name']} ({row['category']}): Телефон {row['phones']}\n"
        return response

    def query_contacts(self, query):
        # Основная функция для запроса
        self.create_embeddings()

        # Поиск по запросу
        results = self.search(query)

        # Генерация ответа
        return self.generate_response(results)