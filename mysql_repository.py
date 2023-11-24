def insert_query(table):
    #insertar los datos
    if table == 'assistant':
        return f"INSERT INTO {table}(uid, role, content, date) VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 MINUTE))"
    elif table == 'users':
        return f"INSERT INTO {table}(uid, role, content, date) VALUES (%s, %s, %s, NOW())"
