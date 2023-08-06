import os
global DEFAULT_LOC
DEFAULT_LOC = os.environ['HOME']
global DEFAULT_TABLE_COL
DEFAULT_TABLE_COL = "(action varchar(20),name varchar(200),source varchar(1000),dest varchar(1000),size varchar(50),md5 varchar(50));"
import sqlite3


def get_db_record(TableName,hash,conn):
    try:
        cur=conn.cursor()
        print("create connection OK")
        sql1 = sql1 = "select action,source,md5 from " + TableName + " where " + TableName + ".action = " + "'new' and " + TableName + ".md5 = " + "'" + md5+"'" + ";" 
        print(sql)
        cur.execute(sql)
        print("select OK")
        return cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
      print("Get Data Error," + e)

def update_db_record(tablename,csvfile,conn):
    global DEFAULT_CREATE_TABLE_SQL
    try:
        cur=conn.cursor()
        print("create connection OK")       
        f = open(csvfile, 'r',newline='')
        csvreader = csv.reader(f)
        list1 = list(csvreader)
        sql = "insert into " + tablename + " values(?,?,?,?,?,?);"
        ###for postgresql else : sql = "insert into " + tablename + " values(%s,%s,%s,%s,%s);"
        cur.executemany(sql,list1)
        conn.commit()        
        cur.close()
        conn.close()
    except Exception as e:
        print("Insert Data Error," + str(e))


def init_db(dbname):
    global DEFAULT_LOC
    if os.path.exists(os.path.join(DEFAULT_LOC,dbname+".db")):
        os.remove(os.path.join(DEFAULT_LOC,dbname+".db"))
    conn = sqlite3.connect(os.path.join(DEFAULT_LOC,dbname+".db"))
    return conn

def get_db(dbname):
    global DEFAULT_LOC
    conn = sqlite3.connect(os.path.join(DEFAULT_LOC,dbname+".db"))
    return conn


def init_db_table(conn,tablename):
    cur = conn.cursor()  
    sql1 = "drop table if exists "+tablename+";";
    cur.execute(sql1)
    print("drop table OK")
    sql2 = "create table " + tablename + DEFAULT_CREATE_TABLE_SQL
    cur.execute(sql2)
    print("create table OK")
    return conn


def init_log(logname):
    global DEFAULT_LOC
    log_name = os.path.join(DEFAULT_LOC,logname)
    if os.path.exists(log_name):
        os.remove(log_name)
    f = open(log_name,'w')
    f.close() 
    return log_name


    
