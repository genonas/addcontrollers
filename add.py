import psycopg2
import logging


#данные для подключения к БД PostgresSQL
db_name = '' #имя БД
db_user = '' #имя пользователя
db_password = '' #пароль
db_host = 'localhost' #хост
db_port = '5432' #порт БД (по умолчанию 5432)

#id ленты координации
lk = 4
#кол-во контроллеров 
c = 1

#Стартовые координаты
x = 87.1663693833798 #далее по коду увеличивается на +0.01
y = 53.7837930946674

programid=[]
phaseid=[]
planidall=[]

#Cоздание контроллера
def addСontroller(countcontroller):
    global lk
    global x
    global programid
    global phaseid
    global planidall
    for i in range(0,countcontroller):    
        #Создание контроллера в БД
        insert_query = 'INSERT INTO controller (name,ip,port,location,model,active,has_spot,spot_port,has_countdown_board,countdown_board_port,local_adaptive_on,marked,reversible,visually_impaired) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
         #Создание координат   
        coordinates = f"{x}, {y}"
        insert_data = ('test_1','127.0.0.15',161,coordinates,'Sintez-D',True,False,8090,False,0,False,False,False,False)
        cursor.execute(insert_query,insert_data)
        conn.commit()
        x+=0.01
        #получение id у созданного контроллера
        select_query = 'select id from controller order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            controllerid = row[0]

        #Запрос на добавление фаз
        insert_query_three = 'INSERT INTO phase (phase_number,opng_tact,clsg_tact,secure_time,adaptive_min_time,adaptive_max_time,controllerid) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        for plan in range(1,9):
            insert_data_three = (plan,3,3,15,16,20,controllerid)
            cursor.execute(insert_query_three,insert_data_three)
            conn.commit()

            select_query = 'select id from phase order by id desc limit 1'
            cursor.execute(select_query)
            for row in cursor:
                phaseid.append(row[0])

        #Запрос на создание плана
        insert_query_two = 'INSERT INTO plan (name,type,active,controllerid) VALUES (%s,%s,%s,%s)'
        plan_name = 'test_' + str(i)
        insert_data_two = (plan_name,'20_CENTRAL',False,controllerid)
        cursor.execute(insert_query_two,insert_data_two)
        conn.commit()

        #Запрос на planid
        select_query = 'select id from plan order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            plan_id = row[0]
            planidall.append(row[0])    

        #Запрос на создание плана ЦУ
        insert_query = 'INSERT INTO program (shift,conditions_type,conditions,mode,planid) VALUES (%s,%s,%s,%s,%s)'

        insert_data = (0,'TIME','{"days":127,"start_time":"02:00:00","end_time":"04:00:00"}','PHASES',plan_id)
        cursor.execute(insert_query,insert_data)
        conn.commit()

        select_query = 'select id from program order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            programid.append(row[0])

    
        insert_data = (0,'TIME','{"days":127,"start_time":"04:00:00","end_time":"06:00:00"}','PHASES',plan_id)
        cursor.execute(insert_query,insert_data)
        conn.commit()

        select_query = 'select id from program order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            programid.append(row[0]) 

        insert_data = (0,'TIME','{"days":127,"start_time":"06:00:00","end_time":"12:00:00"}','PHASES',plan_id)
        cursor.execute(insert_query,insert_data)
        conn.commit()

        select_query = 'select id from program order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            programid.append(row[0]) 

        insert_data = (0,'TIME','{"days":127,"start_time":"12:00:00","end_time":"15:00:00"}','PHASES',plan_id)
        cursor.execute(insert_query,insert_data)
        conn.commit()

        select_query = 'select id from program order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            programid.append(row[0]) 

        insert_data = (0,'TIME','{"days":127,"start_time":"15:00:00","end_time":"00:00:00"}','PHASES',plan_id)
        cursor.execute(insert_query,insert_data)
        conn.commit()

        select_query = 'select id from program order by id desc limit 1'
        cursor.execute(select_query)
        for row in cursor:
            programid.append(row[0])

        #Запрос на создание программы плана
        for j in range(0,8):
            insert_query = 'INSERT INTO programsphases (phase_order,phase_time,programid,phaseid) VALUES (%s,%s,%s,%s)'
            for d in range(0,5):
                insert_data = (j,15,programid[d],phaseid[j])
                cursor.execute(insert_query,insert_data)
                conn.commit()
        programid.clear()
        phaseid.clear()
    
    for k in range(0,(len(planidall))):

        insert_query = 'INSERT INTO plantoplangroup (planid,plangroupid) VALUES (%s,%s)'

        insert_data = (planidall[k],lk)
        cursor.execute(insert_query,insert_data)
        conn.commit()

if __name__=='__main__':
    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user, 
            password=db_password,
            host=db_host,
            port=db_port
            )
        cursor = conn.cursor()
        addСontroller(c) 

        cursor.close()
        conn.close()
    except Exception as e:
        logging.error('Ошибка')
        logging.exception(e)