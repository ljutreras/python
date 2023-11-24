def insert_query(table, rol):
    #insertar los datos
    if table == 'users':
        if rol == 'user':
            return f"INSERT INTO {table}(uid, role, content, date, b_id) VALUES (%s, %s, %s, NOW(), LAST_INSERT_ID())"
        else:
            return f"INSERT INTO {table}(uid, role, content, date, b_id) VALUES (%s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 SECOND), LAST_INSERT_ID())"


    elif table == 'bots':
        return f"INSERT INTO {table}(company, system_role) VALUES (%s, %s)"
