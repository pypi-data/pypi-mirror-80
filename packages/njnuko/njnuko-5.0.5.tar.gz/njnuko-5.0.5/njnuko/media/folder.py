import os
import os.path
import csv
from Media_File import Media_File 
from file import *
from log import *


global DEFAULT_DB
DEFAULT_DB = "njnuko"

def check_folder(folder):
    check_log = init_log(os.path.basename(folder)+'_check.log')
    global checking
    checking = []
    check_log = process_checking(folder,check_log)
    conn = init_db(DEFAULT_DB)
    init_db_table(os.path.basename(folder))
    update_db_record(os.path.basename(folder),check_log,conn)
    return check_log

def process_checking(folder,log):
    global checking
    for i in os.listdir(folder):            
        if os.path.isdir(os.path.join(folder,i)):
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_checking(os.path.join(folder,i),log)
        else:
            media = Media_File(os.path.join(folder,i))
            hash = media.get_md5()
            if hash is not None:
                if hash in checking:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['duplicate',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                    os.remove(os.path.join(folder,i)) 
                else:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['new',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                    checking.append(hash)

def compare_folder(cmp_folder,std_table):
    """
    用来对比文件夹cmp_folder和文件夹cmp_folder
    如果cmp_foler中的文件在ctd_folder中，则删除
    """
    global compare
    compare = []
    check_log = init_log(os.path.basename(std_table)+'_check.log')
    cmp_log = init_log(os.path.basename(cmp_folder)+'_comp.log')
    check_log=check_folder(std_table)
    conn = get_db("njnuko")
    cmp_log=process_comparing(cmp_folder,os.path.basename(std_table),cmp_log,conn)
    init_db_table(os.path.basename(cmp_folder))
    update_db_record(os.path.basename(cmp_folder),cmp_log,conn)
    return cmp_log

def process_comparing(folder,tablename,log,conn):
    global get_db_record_sql
    for i in os.listdir(folder):
        if os.path.isdir(os.path.join(folder,i)):
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_comparing(os.path.join(folder,i),tablename,log,conn)
        else:
            media = Media_File(os.path.join(folder,i))
            hash = media.get_md5()
            if hash is not None:
                a = get_db_record(tablename,hash,conn)
                if a is not None:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['compare',i,os.path.join(folder,i),a[1],os.path.getsize(os.path.join(folder,i)),hash])
                    os.remove(os.path.join(folder,i))
                else:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['new',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])                   
                        compare.append(hash)  
 
