def formas_y_lugares_de_pago():
    """proporcionan las formas y lugares de pago que tiene un usuario mediante un formato predefinido entre triple comillas dobles

    Args:
        message (str): se entregará una opcion valida del servicio de formas y lugares de pago

    Returns:
        prompt (str): genera una respuestas la cual incluye las formas y lugares de pago
    """
      
    prompt: str = f"""
                FORMAS Y LUGARES DE PAGO 
                En Movistar te brindamos diversas formas de pago SIN COMISIÓN. \
                Puedes pagar por Yape \
                https://innovacxion.page.link/mVFa \
                desde la web o app de tu banco. \
                Conoce todos los canales de pago en el siguiente link \
                https://www.movistar.com.pe/atencion-al-cliente/lugares-y-medios-de-pago
            """
    return prompt
