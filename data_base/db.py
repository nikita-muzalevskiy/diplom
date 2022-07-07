import sqlite3 as sq
from PGdb import (query, query_no_ret)

def sqlite_start():
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    if base:
        print('Database is connected')
    base.execute('CREATE TABLE IF NOT EXISTS main_table (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                 '                                       shop TEXT,'
                 '                                       category TEXT,'
                 '                                       payment_date DATETIME,'
                 '                                       sum MONEY )')

#Для добавления записей в расходы
def DBinsert(shop, cat, date, sum):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    ins = f"INSERT INTO main_table (shop, category, payment_date, sum_val) VALUES ('{shop}', '{cat}', '{date}', {sum})"
    base.execute(ins)
    base.commit()

#Для добавления записей в доходы
def DBinsert_profit(cat, date, sum):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    ins = f"INSERT INTO profit_table (category, payment_date, sum_val) VALUES ('{cat}', '{date}', {sum})"
    base.execute(ins)
    base.commit()

def get_column(date1, date2):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = f"SELECT * FROM main_table WHERE payment_date >= '{date1}' AND payment_date <= '{date2}'"
    cur.execute(select)
    records = cur.fetchall()
    my_list = list()
    my_list.clear()
    for row in records:
        my_list.append(row)
    base.commit()
    cur.close()
    print(my_list)
    return my_list

def get_column_profit(date1, date2):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = f"SELECT * FROM profit_table WHERE payment_date >= '{date1}' AND payment_date <= '{date2}'"
    cur.execute(select)
    records = cur.fetchall()
    my_list = list()
    my_list.clear()
    for row in records:
        my_list.append(row)
    base.commit()
    cur.close()
    print(my_list)
    return my_list

#Возвращает список магазинов списком (list)
def get_list(table):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = f"SELECT name FROM {table}"
    cur.execute(select)
    records = cur.fetchall()

    my_list = list()
    for row in records:
        my_list.append(row[0])
    base.commit()
    cur.close()
    return my_list

# Вариант для PG
# def get_list(table):
#     query = f"SELECT name FROM {table} WHERE user_id = 1"
#     records = PGdb.query(query)
#     my_list = list()
#     for row in records:
#         my_list.append(row[0])
#     return my_list

def db_delete(name, table):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    delete = f'DELETE from {table} where name = "{name}"'
    cur.execute(delete)
    base.commit()
    cur.close()

def db_insert(name, table):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    insert = f'INSERT INTO {table} (name) VALUES ("{name}")'
    cur.execute(insert)
    base.commit()
    cur.close()

def get_count(name, table):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = f'SELECT COUNT (*) name FROM {table} WHERE name = "{name}"'
    cur.execute(select)
    records = cur.fetchall()

    for row in records:
        count = row[0]
    base.commit()
    cur.close()
    return count

def queryLite_no_ret(q):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    cur.execute(q)
    base.commit()
    cur.close()

def queryLite(q):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    cur.execute(q)
    records = cur.fetchall()
    base.commit()
    cur.close()
    return records

def autofillLite():
    file = open("user.txt", "r")
    file.seek(0)
    id = file.readlines()[1]

    table = query(f"SELECT * FROM category WHERE user_id = {id}")
    count = query(f"SELECT COUNT(*) FROM category WHERE user_id = {id}")[0][0]
    for i in range(count):
        queryLite_no_ret(f"INSERT INTO category (name) VALUES ('{table[i][1]}')")

    table = query(f"SELECT * FROM category_profit WHERE user_id = {id}")
    count = query(f"SELECT COUNT(*) FROM category_profit WHERE user_id = {id}")[0][0]
    for i in range(count):
        queryLite_no_ret(f"INSERT INTO category_profit (name) VALUES ('{table[i][1]}')")

    table = query(f"SELECT * FROM shops WHERE user_id = {id}")
    count = query(f"SELECT COUNT(*) FROM shops WHERE user_id = {id}")[0][0]
    for i in range(count):
        queryLite_no_ret(f"INSERT INTO shops (name) VALUES ('{table[i][1]}')")

    table = query(f"SELECT * FROM main_view WHERE user_id = {id}")
    count = query(f"SELECT COUNT(*) FROM main_view WHERE user_id = {id}")[0][0]
    for i in range(count):
        queryLite_no_ret(f"INSERT INTO main_table (shop, category, payment_date, sum_val) VALUES ('{table[i][2]}', '{table[i][3]}', '{table[i][4]}', {table[i][5]})")

    table = query(f"SELECT * FROM profit_view WHERE user_id = {id}")
    count = query(f"SELECT COUNT(*) FROM profit_view WHERE user_id = {id}")[0][0]
    for i in range(count):
        queryLite_no_ret(f"INSERT INTO profit_table (category, payment_date, sum_val) VALUES ('{table[i][2]}', '{table[i][3]}', {table[i][4]})")

def autofillPG():
    file = open("user.txt", "r")
    file.seek(0)
    id = file.readlines()[1]

    table = queryLite("SELECT * FROM category")
    count = queryLite("SELECT COUNT(*) FROM category")[0][0]
    for i in range(count):
        query_no_ret(f"INSERT INTO category (name, user_id) VALUES ('{table[i][0]}', {id})")

    table = queryLite("SELECT * FROM category_profit")
    count = queryLite("SELECT COUNT(*) FROM category_profit")[0][0]
    for i in range(count):
        query_no_ret(f"INSERT INTO category_profit (name, user_id) VALUES ('{table[i][0]}', {id})")

    table = queryLite("SELECT * FROM shops")
    count = queryLite("SELECT COUNT(*) FROM shops")[0][0]
    for i in range(count):
        query_no_ret(f"INSERT INTO shops (name, user_id) VALUES ('{table[i][0]}', {id})")

    table = queryLite("SELECT * FROM main_table")
    count = queryLite("SELECT COUNT(*) FROM main_table")[0][0]
    for i in range(count):
        shop_id = query(f"SELECT id from shops WHERE name = '{table[i][1]}' AND user_id = {id}")
        category_id = query(f"SELECT id from category WHERE name = '{table[i][2]}' AND user_id = {id}")
        query_no_ret(f"INSERT INTO main (user_id, shop, category, date, sum) VALUES ({id}, {shop_id[0][0]}, {category_id[0][0]}, '{table[i][3]}', {table[i][4]});")

    table = queryLite("SELECT * FROM profit_table")
    count = queryLite("SELECT COUNT(*) FROM profit_table")[0][0]
    for i in range(count):
        category_id = query(f"SELECT id from category_profit WHERE name = '{table[i][1]}' AND user_id = {id}")
        query_no_ret(f"INSERT INTO profit_main (user_id, category_profit, date, sum) VALUES ({id}, {category_id[0][0]}, '{table[i][2]}', {table[i][3]});")


def autodeleteLite():
    queryLite_no_ret("DELETE FROM category")
    queryLite_no_ret("DELETE FROM category_profit")
    queryLite_no_ret("DELETE FROM shops")
    queryLite_no_ret("DELETE FROM main_table")
    queryLite_no_ret("DELETE FROM profit_table")

def autodeletePG():
    file = open("user.txt", "r")
    file.seek(0)
    id = file.readlines()[1]

    query_no_ret(f"DELETE FROM main WHERE user_id = {id}")
    query_no_ret(f"DELETE FROM profit_main WHERE user_id = {id}")
    query_no_ret(f"DELETE FROM shops WHERE user_id = {id}")
    query_no_ret(f"DELETE FROM category WHERE user_id = {id}")
    query_no_ret(f"DELETE FROM category_profit WHERE user_id = {id}")