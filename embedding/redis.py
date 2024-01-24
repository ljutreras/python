import csv
import embedding.redis as redis


r = redis.Redis(host='localhost', port=6379, db=0, hash_name='qa')

questions = []
answers = []

with open('/Users/leona/Downloads/Q_A_CHATBOT_GARANTIZAR-V2-.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      question = row[1]
      answer = row[2]
      r.hset('qa', question, answer)

for key in r.hkeys('qa'):
        questions.append(key.decode('utf-8'))

for key in r.hkeys('qa'):
    answers.append(r.hget('qa', key).decode('utf-8'))

qa_dict = dict(zip(questions, answers))

print(qa_dict)