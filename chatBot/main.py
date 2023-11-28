import openai

# Aquí configuras tu API key de OpenAI
api_key = "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"
openai.api_key = api_key

# Función para enviar mensajes al modelo y obtener la respuesta
def enviar_al_modelo(prompt):
    response = openai.Completion.create(
      engine="gpt-3.5-turbo-1106",
      prompt=prompt,
      max_tokens=100
    )
    return response.choices[0].text.strip()

# Función para manejar la interacción con el usuario
def chatbot_telefonica():
    print("¡Hola! Soy el chatbot de Telefónica PE. ¿En qué puedo ayudarte hoy?")
    while True:
        print("Opciones disponibles:")
        print("1. Verificar saldo")
        print("2. Pagar factura")
        print("3. Salir")
        
        opcion = input("Selecciona una opción (1/2/3): ")

        if opcion == "1":
            verificar_saldo()
        elif opcion == "2":
            pagar_factura()
        elif opcion == "3":
            print("¡Hasta luego! Gracias por usar el servicio de Telefónica PE.")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

# Función para verificar el saldo del usuario
def verificar_saldo():
    # Aquí implementa la lógica para verificar el saldo
    # Si el usuario no está registrado, solicita los datos para registrarlo
    # Consulta la información de la cuenta del usuario y muestra el saldo actual
    # Responde al usuario con el saldo actual

    respuesta = "Respuesta personalizada de verificación de saldo."
    print(respuesta)

# Función para pagar una factura
def pagar_factura():
    # Aquí implementa la lógica para pagar una factura
    # Verifica si el usuario está registrado, si no, pide los datos para registrarlo
    # Solicita al usuario el ID de la factura a pagar
    # Obtiene el monto de la factura según el ID proporcionado
    # Procesa el pago y confirma al usuario
    
    respuesta = "Respuesta personalizada de pago de factura."
    print(respuesta)

# Ejecutar el chatbot
chatbot_telefonica()
