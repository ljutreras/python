def detalle_de_la_deuda():
    """proporciona el detalle de la deuda de un usuario mediante un formato predefinido entre triple comillas dobles

    Returns:
        prompt (str): proporciona un detalle de la deuda del usuario
    """        
        
    prompt: str = f"""
            DETALLE DE LA DEUDA
            Estimado client@
            Tienes un recibo pendiente de tu servicio <MOVIL/HOGAR> N° Servicio 7556 
            que venció el 09/23 por CLP 25.000
            """
    return prompt
