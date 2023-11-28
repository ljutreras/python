from db.mysql_repository import connect_to_database

def insert_db(uid, role, content, function_calling ,id_bot):
    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        if role == 'user':
            insert_query = "INSERT INTO chats(uid, role, content, function_calling, date, id_bot) VALUES(%s, %s, %s, %s, NOW(), %s)"
            cursor.execute(insert_query, (uid, role, content, function_calling, id_bot))
        elif role == 'assistant':
            insert_query = "INSERT INTO chats(uid, role, content,function_calling, date, id_bot) VALUES(%s, %s, %s, %s, DATE_ADD(NOW(), INTERVAL 1 SECOND), %s)"
            cursor.execute(insert_query, (uid, role, content, function_calling,id_bot))

        connection.commit()
        cursor.close()
        connection.close()