import psycopg2


DB_URI="postgres://bxilbbud:SsuWC0gTuxiD4tg3GtnsVFL__Jt1BhMk@manny.db.elephantsql.com/bxilbbud"


conn = psycopg2.connect(DB_URI,sslmode="require")
cursor = conn.cursor()


async def sql_start(message,ID:str,username:str,user_class:str,role:str):

    cursor.execute(f"SELECT * FROM public.users WHERE ID='{ID}'")
    pin2 = cursor.fetchone()

    if pin2 == None:
        cursor.execute('INSERT INTO public.users (ID,username,user_class,role) VALUES(%s,%s,%s,%s)',(ID,username,user_class,role))
        conn.commit()
    else:
        x = pin2[2].replace(" ", "")
        if x != user_class:
            cursor.execute(f"UPDATE public.users SET user_class='{user_class}' WHERE ID='{ID}'")
            await message.answer('Класс обновлен!')


async def check_for_admin(id):
    cursor.execute(f"SELECT * FROM public.users WHERE ID='{id}'")
    pin2 = cursor.fetchone()
    role=pin2[3]
    role=role.replace(" ","")
    return role

async def check_class(id):
    cursor.execute(f"SELECT * FROM public.users WHERE ID='{id}'")
    pin2 = cursor.fetchone()
    user_class = pin2[2]
    user_class = user_class.replace(" ", "")
    return user_class

async def sql_home_work(subject:str, homework:str, user_class:str):
    cursor.execute(f"SELECT * FROM public.home_work WHERE subject='{subject}' AND user_class='{user_class}'")
    result=cursor.fetchone()
    if result != None:
        cursor.execute(f"UPDATE public.home_work  SET subject='{subject}',homework='{homework}' WHERE subject='{subject}' AND user_class='{user_class}'")
        conn.commit()
    else:
        cursor.execute("INSERT INTO public.home_work (subject,homework,user_class) VALUES(%s,%s,%s)",(subject,homework,user_class))
        conn.commit()


async def sql_time_table(Day:str,l_1:str,l_2:str,l_3:str,l_4:str,l_5:str,l_6:str,l_7:str,user_class:str):
    cursor.execute(f"SELECT * FROM public.time_table WHERE day='{Day}' AND user_class='{user_class}'")
    result=cursor.fetchone()
    if result==None:
        cursor.execute(
            "INSERT INTO public.time_table (day,l_1,l_2,l_3,l_4,l_5,l_6,l_7,User_Class) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (Day, l_1, l_2, l_3, l_4, l_5, l_6, l_7, user_class))
        conn.commit()
    else:
        cursor.execute(
            f"UPDATE public.time_table SET l_1='{l_1}',l_2='{l_2}',l_3='{l_3}',l_4='{l_4}',l_5='{l_5}',l_6='{l_6}',l_7='{l_7}' WHERE day='{Day}' AND user_class='{user_class}'")
        conn.commit()

async def sql_check_tb(message, Day, id):
    cursor.execute(f"SELECT * FROM public.users WHERE ID='{id}'")
    pin2 = cursor.fetchone()
    User_Class = pin2[2]
    cursor.execute(f"SELECT * FROM public.time_table WHERE Day='{Day}' AND user_class='{User_Class}'")
    pin1 = cursor.fetchone()
    if pin1 == None:
        await message.answer('Сорри,у меня нет такой информации')
    else:
        await message.answer(f"День недели: {pin1[0]}\n1.{pin1[1]}\n2.{pin1[2]}\n3.{pin1[3]}\n4.{pin1[4]}\n5.{pin1[5]}\n6.{pin1[6]}\n7.{pin1[7]}")

async def sql_check_hw(message, sub, id):
    cursor.execute(f"SELECT * FROM public.users WHERE ID='{id}'")
    pin2 = cursor.fetchone()
    User_Class = pin2[2]
    cursor.execute(f"SELECT * FROM public.home_work WHERE subject='{sub}' AND user_class='{User_Class}'")
    pin1 = cursor.fetchone()

    if pin1 != None:
        sub = pin1[0].replace(" ", "")
        await message.answer(f"{sub}:\n{pin1[1]}")
    else:
        await message.answer('Ошибка:\nЛибо ты неправильно написал предмет,либо админ не добавил домашку по этому предмету')

async def change_role(user_id,x):
    cursor.execute(f"UPDATE public.users SET role='{x}' WHERE id='{user_id}'")
    conn.commit()


async def hw_tomorrow(message,id,Day):
    cursor.execute(f"SELECT * FROM public.users WHERE ID='{id}'")
    pin2 = cursor.fetchone()
    User_Class = pin2[2]
    cursor.execute(f"SELECT l_1,l_2,l_3,l_4,l_5,l_6,l_7 FROM public.time_table WHERE Day='{Day}' AND user_class='{User_Class}'")
    pin3 = cursor.fetchone()
    pin1 = list(set(pin3))
    y = 0
    await message.answer(f'Завтра {Day}')
    for i in pin1:
        cursor.execute(f"SELECT homework FROM public.home_work WHERE user_class='{User_Class}' and subject='{i}'")
        x = cursor.fetchone()
        if x != None and x != '-':
            y += 1
            await message.answer(f"{i}\n{x[0]}")
    if y == 0:
        await message.answer("Ничего не задали)")

