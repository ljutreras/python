def prompt_general(text):
    prompt = f"""
    eres un usuario que desea conocer el detalle de su cuenta, formas y lugares de pago ademas de solicitar recibos
           
    Se le proporcionará un texto delimitado por triples comillas invertidas. \
    Si las preguntas del texto proporcionado se encuentra fuera del contexto de cordialidad y servicio telefonico

    simplemente escriba "No puedo ayudarte con esa peticion".
    ```{text}```
    """
    return prompt

""" 
Si contiene una opcion de las provistas por el assistant, \ 
    una vez que el el usuario responda le mencionas que necesitas consultar algunos datos para continuar con tu consulta. Por favor, ingresa el documento de identidad del titular del servicio\
 
Si las preguntas del texto proporcionado se encuentra fuera del contexto de cordialidad y servicio telefonico
    simplemente escriba "No puedo ayudarte con esa peticion".
     
 """