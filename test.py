async def run_conversation(user: User):
        user_id = uid if user.id == None else user.id
        res = user.message
        try:
            # Step 1: send the conversation and available functions to the model
            messages=[
                {
                    'role': 'system',
                    'content':'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha'
                },
                {
                    'role':'user',
                    'content': res
                }
            ]
            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "get_date_from_body",
                        "description": "give an response with an external date, not the wheater",
                        "parameters": {
                            "type": "object",
                            "properties": {}
                        },
                    },
                }
            ]
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                messages=messages,
                tools=tools,
                tool_choice='auto'
            )
            response_message = response.choices[0].message

            tool_calls = response_message.tool_calls
            # Step 2: check if the model wanted to call a function
            if tool_calls:
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                available_functions = {
                    "get_date_from_body": get_date_from_body,
                }
                messages.append(response_message)  # extend conversation with assistant's reply
                # Step 4: send the info for each function call and function response to the model
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_response = function_to_call()
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    ) 
                second_response = openai.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                )
                
                # if connection:
                #     #cursor.execute(insert_query('bots'),('onbotgo', 'Eres una agente virtual llamada MIA y tu objetivo es decir la fecha'))
                #     cursor.execute(insert_query('users'),(uid, second_response.choices[0].message.role, second_response.choices[0].message.content))
                #     cursor.execute(insert_query('users'),(uid, 'user', res))
                #     connection.commit()
                #     cursor.close()
                #     connection.close()
                    
                return {'id': user_id, 'message':second_response.choices[0].message.content}
            else:
                 print(f'else: {response_message}')
                 return {'message': response_message.content}
        except TypeError as e:
            return e