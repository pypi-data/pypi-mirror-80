import os
import os.path
import stat
import time
import csv
import sqlite3
import imagehash
from folder import *
from file import *
#引入folder里面的通用函数，例如file_move,get_db,update_db


def class_bysize(folder,dstfold,large=1):
    home = os.environ['HOME']
    class_by_size_log = os.path.join(home,os.path.basename(folder)+'_class_by_size.log')
    os.makedirs(os.path.join(dstfold,"large"))
    os.makedirs(os.path.join(dstfold,"small"))
    if os.path.exists(class_by_size_log):
        os.remove(class_by_size_log)
    f = open(class_by_size_log,'w')
    f.close()  
    process_bysize(folder,dstfold,class_by_size_log,large)
    return class_by_size_log


def class_bytype(folder,dstfold):
    home = os.environ['HOME']
    class_by_type_log = os.path.join(home,os.path.basename(folder)+'_class_by_type.log')
    if os.path.exists(class_by_type_log):
        os.remove(class_by_type_log)
    f = open(class_by_type_log,'w')
    f.close()      
    process_bytype(folder,dstfold,class_by_type_log)


def class_bytime(folder,desfold):
    log = os.path.join(desfold,'class_bytime.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()      
    process_bytime(folder,desfold,log)


def class_bymaker(folder,desfold):
    log = os.path.join(desfold,'class_bymaker.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()      
    process_bymaker(folder,desfold,log)



#################################################################

def process_bysize(folder,dstfold,log,large):

    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bysize(os.path.join(folder,i),dstfold,log,large)
            else:
                size = os.path.getsize(os.path.join(folder,i))
                if size < large*1024*1024:
                    file_move(folder,i,os.path.join(dstfold,"large"),log)
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['move',i,os.path.join(folder,i),os.path.join(dstfold,"large"),size,''])
                        f.close()    
                else:
                    file_move(folder,i,os.path.join(dstfold,"small"),log)
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['move',i,os.path.join(folder,i),os.path.join(dstfold,"small"),size,''])
                        f.close()     

def process_bytype(folder,dstfold,log):

    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bytype(os.path.join(folder,i),dstfold,log)
            else:
                media = Media_File(os.path.join(folder,i))
                type = media.get_type()
                if not (os.path.exists(os.path.join(dstfold,type))):
                    os.makedirs(os.path.join(dstfold,type))
                result=file_move(os.path.join(folder,i),os.path.join(dstfold,type))
                with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(result)



def process_bytime(folder,desfold,log):
    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bytime(os.path.join(folder,i),desfold,log)
            else:
                media = Media_File(os.path.join(folder,i))
                a = media.get_create_date()          
                if not os.path.exists(os.path.join(desfold,a)):
                    os.makedirs(os.path.join(desfold,a))
                temp_log = file_move(folder,i,os.path.join(desfold,a))
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(temp_log)
               
def process_bymaker(folder,desfold,log):
    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bymaker(os.path.join(folder,i),desfold,log)
            else:            
                media = Media_File(os.path.join(folder,i))
                maker = media.get_maker(os.path.join(folder,i))
                if not os.path.exists(os.path.join(desfold,maker)):
                    os.makedirs(os.path.join(desfold,maker))
                temp_log = file_move(folder,i,os.path.join(desfold,maker))   
                with open(log,'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(temp_log)             


