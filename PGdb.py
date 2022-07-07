import psycopg2
from psycopg2 import Error

def query(query):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="1305",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="diplom")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        cursor.execute(query)
        # Получить результат
        record = cursor.fetchall()
        return record

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

def query_no_ret(query):
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="1305",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="diplom")

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # Выполнение SQL-запроса
        cursor.execute(query)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            connection.commit()
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")