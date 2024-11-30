import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
class ContactSearch:
    def __init__(self, file_path, model_name='paraphrase-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.file_path = file_path
        self.data = self.load_data()
        self.create_embeddings()
#вынести отдельно contact
    def load_data(self):
        return pd.read_csv(self.file_path, delimiter=';')

    def create_embeddings(self):
        if 'embedding' not in self.data.columns:
            self.data['text'] = self.data.apply(lambda x: f"{x['category']} {x['name']}", axis=1)
            self.data['embedding'] = self.data['text'].apply(lambda x: self.model.encode(x))

    def search(self, query, top_k=10):

        query_vec = self.model.encode(query)

        self.data['similarity'] = self.data['embedding'].apply(
            lambda x: np.dot(query_vec, x) / (np.linalg.norm(query_vec) * np.linalg.norm(x))
        )

        filtered_data = self.data[self.data['similarity'] >= 0.5]

        results = filtered_data.sort_values(by='similarity', ascending=False).head(top_k)
        return results[['id', 'name', 'category', 'phones', 'add_phone']]

    def generate_response(self, results):
        if results.empty:
            return None
        response = "Вот что удалось найти:\n"
        for _, row in results.iterrows():
            response += f"- {row['name']} ({row['category']}): Телефон {row['phones']}\n"
        return response

    def query_contacts(self, query):
        self.create_embeddings()
        results = self.search(query)
        return self.generate_response(results)
