import sqlite3, random, time
from russian_names import RussianNames as RN
from datetime import date

conn = sqlite3.connect("usingdb.db")
cursor = conn.cursor()

def gen_data():
    #data troubles
    s_year = date.today().year-100

    year = random.randint(s_year, date.today().year)

    if year == s_year:
        month = random.randint(date.today().month, 12)
    elif year == date.today().year:
        month = random.randint(1, date.today().month)
    else:
        month = random.randint(1, 12)

    if year == date.today().year and month == date.today().month:
        day = random.randint(1, date.today().day)
    else:
        if month == 2:
            if year%4 == 0:
                day = random.randint(1, 29)
            else:
                day = random.randint(1, 28)
        elif month == 4 or month == 6 or month == 9 or month == 11:
            day = random.randint(1, 30)
        else:
            day = random.randint(1, 31)

    return date(year, month, day)

def function1():
    cursor.execute("""CREATE TABLE IF NOT EXISTS basedata
    (FIO, DateOfBurth DATE, Gender)
    """)
    conn.commit()

def function2(FIO, DateOfBurth, Gender):
    cursor.execute("INSERT INTO basedata(FIO, DateOfBurth, Gender) VALUES (?, ?, ?)", (FIO, DateOfBurth, Gender))
    conn.commit()

def function3():
    res = list(cursor.execute("""SELECT DISTINCT *,
    strftime('%Y', 'now') - strftime('%Y', DateOfBurth) - 1 + (CASE
        WHEN strftime('%m', 'now') > strftime('%m', DateOfBurth) OR (strftime('%m', 'now') = strftime('%m', DateOfBurth) AND strftime('%d', 'now') > strftime('%d', DateOfBurth))
        THEN 1
        ELSE 0 
        END) AS AGE
                         FROM basedata
                         GROUP BY FIO, DateOfBurth
                         ORDER BY FIO
                         """))
    for i in res:
        for j in i:
            print(j, " ", end="")
        print()

def function4():
    i = 1
    k = RN(count = 100, gender = 1.0, transliterate=True, output_type='list', first_letter = "Ф").get_batch()

    while(i<100):
        FIO = k[i][2] + " " + k[i][0] + " " + k[i][1]
        DateOfBurth = gen_data()
        Gender = "male"
        cursor.execute("INSERT INTO basedata(FIO, DateOfBurth, Gender) VALUES (?, ?, ?)", (FIO, DateOfBurth, Gender))
        conn.commit()
        i +=1

    k = RN(count = 1000, transliterate=True, output_type='list').get_batch()
    i = 1
    while(i<1000):
        FIO = k[i][2] + ' ' + k[i][0] + ' ' + k[i][1]
        DateOfBurth = gen_data()
        Gender = k[i][3]
      #  print(FIO,' ', DateOfBurth, ' ', Gender)
        cursor.execute("INSERT INTO basedata(FIO, DateOfBurth, Gender) VALUES (?, ?, ?)", (FIO, DateOfBurth, Gender))
       # conn.commit()
        i+=1

def function5():
#    start_time = time.time()
#    res = list(cursor.execute("""SELECT DISTINCT *
#                         FROM basedata
#                         WHERE Gender='male' AND FIO LIKE 'F%'
#                         ORDER BY FIO
#                         """))
#    for i in res:
#        for j in i:
#            print(j, " ", end="")
#        print()
#    print(round(time.time()-start_time, 10))

    #этот запрос в среднем на 0.001с быстрее и даёт более постоянное время обработки
    start_time = time.time()
    res = list(cursor.execute("""SELECT DISTINCT FIO, DateOfBurth, Gender
                         FROM basedata
                         WHERE Gender='male' AND FIO LIKE 'F%'                                             
                         ORDER BY FIO
                         """))
    for i in res:
        for j in i:
            print(j, " ", end="")
        print()
    print(round(time.time()-start_time, 10))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print("Формат ввода для команды 2: разделители в строке - пробелы"
      #    "Пример: myApp 2 Zyaberev Albert Vadimovich 1932-03-02 male")

    while(True):
        enter = input().split(" ")
        if enter[0] == 'exit':
            break
        elif enter[1] == "1":
            function1()
        elif enter[1] == "2":
            if enter[2] and enter[3] and enter[4] and enter[5] and enter[6]:
                function2(enter[2]+' '+enter[3]+' '+enter[4], enter[5], enter[6])
            else:
                print("Unrecognized command")
        elif enter[1] == "3":
            function3()
        elif enter[1] == "4":
            function4()
        elif enter[1] == "5":
            start_time = time.time()
            function5()
        else:
            print("Unrecognized command")