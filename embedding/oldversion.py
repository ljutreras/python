import os
from sklearn.neighbors import NearestNeighbors
import numpy as np
import embedding.redis as redis

os.environ["LOKY_MAX_CPU_COUNT"] = "4"
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key=os.getenv('API_KEY')

def questions_and_answers_from_redis(host='localhost', port=6379, db=0, hash_name='qa'):
    r = redis.Redis(host=host, port=port, db=db)

    questions = []
    answers = []

    for key in r.hkeys(hash_name):
        questions.append(key.decode('utf-8'))

    for key in r.hkeys(hash_name):
        answers.append(r.hget(hash_name, key).decode('utf-8'))

    qa_dict = dict(zip(questions, answers))

    return questions, answers, qa_dict

def find_most_similar_question(questions, new_query):
    def generate_embeddings(data, model="text-embedding-ada-002"):
        embeddings = openai.Embedding.create(input=data, model=model)['data']
        return np.array([x.embedding for x in embeddings])

    def train_nearest_neighbors(vectors, n_neighbors=2):
        neigh = NearestNeighbors(n_neighbors=n_neighbors)
        neigh.fit(vectors)
        return neigh

    # Generar embeddings 
    question_vectors = generate_embeddings(questions)

    # Entrenar modelo NearestNeighbors
    neigh = train_nearest_neighbors(question_vectors)

    # Generar embedding para la nueva pregunta
    query_emb = generate_embeddings([new_query])[0]
    query_vector = [query_emb]

    # Encontrar la pregunta más similar
    distances, indices = neigh.kneighbors(query_vector)
    most_similar = questions[indices[0][0]]

    return most_similar

questions, answers, qa_dict = questions_and_answers_from_redis()

query = input('user: ')
result = find_most_similar_question(questions, query)

print(qa_dict[result])
