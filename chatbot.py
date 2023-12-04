from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
from IPython.display import display,HTML
client = OpenAI()

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message.content

def prompt1 ():

    messages =  [  
    {'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
    {'role':'user', 'content':'tell me a joke'},   
    {'role':'assistant', 'content':'Why did the chicken cross the road'},   
    {'role':'user', 'content':'I don\'t know'}  ]

    response = get_completion_from_messages(messages, temperature=1)
    print(response)

def prompt2 ():
    
    messages =  [  
    {'role':'system', 'content':'You are friendly chatbot.'},    
    {'role':'user', 'content':'Hi, my name is Isa'}  ]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

def prompt3 ():
    
    messages =  [  
    {'role':'system', 'content':'You are friendly chatbot.'},    
    {'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)


def prompt4 ():
    
    messages =  [  
    {'role':'system', 'content':'You are friendly chatbot.'},    
    {'role':'user', 'content':'Yes,  can you remind me, What is my name?'}  ]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)

def prompt5 ():
    
    messages =  [  
    {'role':'system', 'content':'You are friendly chatbot.'},
    {'role':'user', 'content':'Hi, my name is Isa'},
    {'role':'assistant', 'content': "Hi Isa! It's nice to meet you. \
    Is there anything I can help you with today?"},
    {'role':'user', 'content':'Yes, you can remind me, What is my name?'}  ]
    response = get_completion_from_messages(messages, temperature=1)
    print(response)


#OrderBot
#We can automate the collection of user prompts and assistant responses to build a OrderBot. The OrderBot will take orders at a pizza restaurant.

def chatBot():
    prompt = ""
    message = []
    while prompt != "exit":
        prompt = input("Usuario: ")
        
        message.append({"role":"user","content":prompt})
        response = get_completion_from_messages(message)
        message.append({"role":"assistant","content":response})
        print("assistant:"+ response)
        
chatBot()
    