import sqlite3 as sq
import matplotlib as mpl
import matplotlib.pyplot as plt

def get_groups(col):
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = f"SELECT {col}, sum(sum_val) FROM main_table GROUP BY {col}"
    cur.execute(select)
    records = cur.fetchall()
    my_list1 = list()
    my_list2 = list()
    my_list1.clear()
    my_list2.clear()
    for row in records:
        my_list1.append(row[0])
        my_list2.append(row[1])
    base.commit()
    cur.close()
    return my_list1, my_list2

def save_dia_s(list1, list2):
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    fig.patch.set_facecolor('#20242d')
    ax = fig.add_subplot()
    ax.patch.set_facecolor('#20242d')
    plt.title('Популярные Магазины')

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

        return my_autopct
    plt.pie(list2, wedgeprops=dict(width=0.4))
    fig.legend(list1, loc='center left', facecolor='#20242d')
    setColorRCParams()
    fig.savefig('diagramsPic/pieS.png')

def save_dia_c(list1, list2):
    data_names = list1
    data_values = list2

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    fig.patch.set_facecolor('#20242d')
    ax = fig.add_subplot()
    ax.patch.set_facecolor('#20242d')
    mpl.rcParams.update({'font.size': 13})
    plt.title('Популярные категории')
    xs = range(len(data_names))

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct, v=val)

        return my_autopct

    setColorRCParams()

    # plt.pie(list2, labels=list1, autopct=make_autopct(list2), wedgeprops=dict(width=0.4))
    plt.pie(list2, wedgeprops=dict(width=0.4))
    fig.legend(list1, loc='center left', facecolor='#20242d')
    fig.savefig('diagramsPic/pieC.png')

def get_month():
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = "SELECT month_year, sum(sum_val) FROM main_table_view GROUP BY month_year ORDER BY year, month LIMIT 6"
    cur.execute(select)
    records = cur.fetchall()
    my_list1 = list()
    my_list2 = list()
    my_list1.clear()
    my_list2.clear()
    for row in records:
        my_list1.append(row[0])
        my_list2.append(row[1])
    base.commit()
    cur.close()
    return my_list1, my_list2

def get_month_plus():
    print("ТА САМАЯ ФУНКЦИЯ")
    list_1, list_2 = get_month()
    global base, cur
    base = sq.connect('main_data_base.db')
    cur = base.cursor()
    select = "SELECT * FROM prognosis_view"
    cur.execute(select)
    records = cur.fetchall()

    select2 = "SELECT count(*) FROM (SELECT * FROM main_table_view GROUP BY month_year ORDER BY month_year DESC LIMIT 7)"
    cur.execute(select2)
    records2 = cur.fetchall()
    count = records2[0][0]-1

    list_3 = list()
    list_3.clear()
    for row in records:
        list_3.append(float(row[1]))
    sum_val = 0.0
    sum_fin = 0.0
    for i in list_3:
        sum_val += i
    for i in list_3:
        if i/sum_val < 0.1:
            sum_fin += i*2
        elif i/sum_val < 0.25:
            sum_fin += i*1.5
        elif i/sum_val < 0.5:
            sum_fin += i*1.2
        else:
            sum_fin += i*1.1
    print("ДО count",sum_fin)
    if count != 0:
        sum_fin /= count
    print("ПОСЛЕ count",sum_fin)
    if len(list_1) != 0:
        list_1.append(str(next_month(list_1[-1])))
        list_2.append(int(sum_fin))
    print("с доп месяцем",list_1,list_2)
    return list_1, list_2

def save_dia_m(list1, list2):
    if len(list1) == 0:
        return
    fig = plt.figure(figsize=(6, 4))
    fig.patch.set_facecolor('#20242d')
    ax = fig.add_subplot()
    ax.patch.set_facecolor('#20242d')
    setColorRCParams()

    # Задать цвета по очереди добавления
    # mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["r", "g", "b"])

    x = list1
    y = list2
    # ax.hist(y)
    ax.bar(x, y)
    ax.grid()
    fig.savefig('diagramsPic/pieM.png')

def save_dia_m_plus(list1: list, list2: list):
    fig = plt.figure(figsize=(6, 4))
    fig.patch.set_facecolor('#20242d')
    ax = fig.add_subplot()
    ax.patch.set_facecolor('#20242d')
    x = list1
    y = list2
    setColorRCParams()
    # ax.hist(y)
    ax.bar(x, y)
    ax.grid()
    fig.savefig('diagramsPic/pieMp.png')
    #
    # fig = plt.figure(figsize=(6, 4))
    # ax = fig.add_subplot()
    #
    # x = list1
    # y = list2
    # # ax.hist(y)
    # ax.bar(x, y)
    # ax.grid()
    # fig.savefig('diagramsPic/pieMp.png')

#Принимает дату в формате MM-YYYY в виде строки и передает следующий месяц в таком же формате
def next_month (s):
    print(s)
    m = s[5] + s[6]
    y = s[0] + s[1] + s[2] + s[3]
    mi = int(m)
    yi = int(y)
    if m == "12":
        m = "01"
        y = str(yi+1)
    else:
        m = str(mi+1)
    if len(m) == 1:
        m = "0" + m
    d = y + "." + m
    print(d)
    return d

def setColorRCParams():
    COLOR = '#c1c1c1'
    mpl.rcParams['text.color'] = COLOR
    mpl.rcParams['axes.labelcolor'] = COLOR
    mpl.rcParams['xtick.color'] = COLOR
    mpl.rcParams['ytick.color'] = COLOR
    mpl.rcParams['grid.color'] = COLOR
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=["#59bf97", "#d1a7ed", "#ffe5b4"])