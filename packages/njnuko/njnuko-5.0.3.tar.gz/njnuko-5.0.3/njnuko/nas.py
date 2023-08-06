import os
import os.path
import shutil
import time
import datetime
import stat
from PIL import Image,ImageFile
from PIL import ImageChops
from PIL.ExifTags import TAGS
import locale
import filetype
import hashlib
import time
import csv
import sqlite3
locale.getdefaultlocale()
import csv
import imagehash

checking = []
compare = []
"""
###########################################################
1. check_files(folder,table_name)
第一个参数是文件夹，第二个是整理后填入sqllit数据库的表名，用于后续的compare
这个function会直接删除重复文件，根据MD5的值来判断
2. compare_files(folder,table)
3. class_bysize(folder,dstfold,large=1)
4. class_bytype(folder,dstfold)
5. class_bytime(folder,desfold)
6. class_bymaker(folder,desfold)
################### Front Function ####################
"""


def check_files(folder,table_name):
    global checking
    checking = []
    log = os.path.join("~",'check_files.log')
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_checking(folder,log)

    InsertData(table_name,log)
    return log

def compare_files(folder,table):
    global compare
    compare = []
    log = os.path.join(os.path.dirname(folder),'compare_files.log')
    print(log)
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_compare(folder,table,log)
    InsertData(table+"comp",log)

    return log
def class_bysize(folder,dstfold,large=1):
    log = os.path.join(dstfold,'class_bysize.log')
    os.makedirs(os.path.join(dstfold,"large"))
    os.makedirs(os.path.join(dstfold,"small"))
    if os.path.exists(log):
        os.remove(log)
    f = open(log,'w')
    f.close()  
    process_bysize(folder,dstfold,log,large)



def class_bytype(folder,dstfold):
    log = os.path.join(dstfold,'class_bytype.log')
    if os.path.exists(log):
        os.remove(log)

    f = open(log,'w')
    f.close()      
    process_bytype(folder,dstfold,log)



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


def process_compare(folder,table,log):

    for i in os.listdir(folder):
        
        if os.path.isdir(os.path.join(folder,i)):
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_compare(os.path.join(folder,i),table,log)
        else:
            hash = ''
            the_md5=hashlib.md5()
            try:
                with open(os.path.join(folder,i), 'rb') as f:
                    the_md5.update(f.read())
                    hash = the_md5.hexdigest()
                if hash in compare:
                    with open(log,'a',newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['duplicate',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])
                    os.remove(os.path.join(folder,i))
                else:
                    a = GetData(table,hash)
                    if a is not None:
                        with open(log,'a',newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(['compare',i,os.path.join(folder,i),a[1],os.path.getsize(os.path.join(folder,i)),hash])
                        os.remove(os.path.join(folder,i))
                    else:
                        b = GetName(table,i)
                        if b is not None:
                            hash1 =  imagehash.average_hash(Image.open(b[2]))
                            hash2 =  imagehash.average_hash(Image.open(os.path.join(folder,i)))
                            if (hash1 == hash2):
                                with open(log,'a',newline='') as f:
                                    writer = csv.writer(f)
                                    writer.writerow(['similar',i,os.path.join(folder,i),b[2],os.path.getsize(os.path.join(folder,i)),hash])
                                os.remove(os.path.join(folder,i))
                            else:
                                with open(log,'a',newline='') as f:
                                    writer = csv.writer(f)
                                    writer.writerow(['samename',i,os.path.join(folder,i),b[2],os.path.getsize(os.path.join(folder,i)),hash])                   
                                    compare.append(hash)  
                        else:
                            with open(log,'a',newline='') as f:
                                writer = csv.writer(f)
                                writer.writerow(['new',i,os.path.join(folder,i),'',os.path.getsize(os.path.join(folder,i)),hash])                   
                                compare.append(hash)  
            except Exception as e:
                print("Error in Compare loop")    


    
def process_checking(folder,log):
    global checking 
    for i in os.listdir(folder):
        
        if os.path.isdir(os.path.join(folder,i)):
            if i[0] not in ['@','.']:
                print(str(os.path.join(folder,i)) + " is not dummy folder")
                process_checking(os.path.join(folder,i),log)
        else:
            hash = ''
            the_md5=hashlib.md5()
            try:
                with open(os.path.join(folder,i), 'rb') as f:
                    the_md5.update(f.read())
                    hash = the_md5.hexdigest()
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
            except Exception as e:
                print("Error in checking loop!")



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
                if filetype.guess(os.path.join(folder,i)) is not None:
                    type = filetype.guess(os.path.join(folder,i)).extension
                    if not (os.path.exists(os.path.join(dstfold,type))):
                        os.makedirs(os.path.join(dstfold,type))
                    file_move(folder,i,os.path.join(dstfold,type),log)

                else:
                    type = 'None'
                    if not (os.path.exists(os.path.join(dstfold,type))):
                        os.makedirs(os.path.join(dstfold,type))
                    file_move(folder,i,os.path.join(dstfold,type),log)



def process_bytime(folder,desfold,log):
    for i in os.listdir(folder):
        if i[0] not in ['@','.']:

            if os.path.isdir(os.path.join(folder,i)):
                process_bytime(os.path.join(folder,i),desfold,log)
            else:            
                a = gettime(os.path.join(folder,i))[0:7]
                if not os.path.exists(os.path.join(desfold,a)):
                    os.makedirs(os.path.join(desfold,a))
                file_move(folder,i,os.path.join(desfold,a),log)


def process_bymaker(folder,desfold,log):
    for i in os.listdir(folder):
        if i[0] not in ['@','.']:
            if os.path.isdir(os.path.join(folder,i)):
                process_bymaker(os.path.join(folder,i),desfold,log)
            else:            
                a = getmaker(os.path.join(folder,i))
                if not os.path.exists(os.path.join(desfold,a)):
                    os.makedirs(os.path.join(desfold,a))
                file_move(folder,i,os.path.join(desfold,a),log)                


def getDB():
    conn = sqlite3.connect(os.path.join("~",'njnuko.db'))
    return conn


def InsertData(TableName,csvfile):
    try:
        conn = getDB()
        cur=conn.cursor()
        print("create connection OK")
        sql1 = "create table " + TableName + " (action varchar(20),name varchar(200),source varchar(1000),dest varchar(1000),size varchar(50),md5 varchar(50));" 
        print(sql1)
        cur.execute(sql1)
        print("create table OK")
        f = open(csvfile, 'r',newline='')
        csvreader = csv.reader(f)
        list1 = list(csvreader)
        sql = "insert into " + TableName + " values(?,?,?,?,?,?);"
        ###for postgresql else : sql = "insert into " + TableName + " values(%s,%s,%s,%s,%s);"
        cur.executemany(sql,list1)
        conn.commit()        
        cur.close()
        conn.close()
    except Exception as e:
      print("Insert Data Error," + e)


def GetData(TableName,md5):
    try:
        conn = getDB()
        cur=conn.cursor()
        print("create connection OK")
        sql1 = "select action,source,md5 from " + TableName + " where " + TableName + ".action = " + "'new' and " + TableName + ".md5 = " + "'" + md5+"'" + ";" 
        print(sql1)
        cur.execute(sql1)
        print("select OK")
        return cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
      print("Get Data Error," + e)

def GetName(TableName,name):
    try:
        conn = getDB()
        cur=conn.cursor()
        print("create connection OK")
        sql1 = "select action,name,source,md5 from " + TableName + " where " + TableName + ".name = " + "'" + name+"'" + ";" 
        print(sql1)
        cur.execute(sql1)
        print("Select OK")
        return cur.fetchone()
        cur.close()
        conn.close()
    except Exception as e:
      print("Get Name Error," + e)



def file_move(frfolder,file1,dest,log):

    if os.path.exists(os.path.join(dest,file1)):
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f2 = open(os.path.join(dest,file1), 'rb')
        the_md5.update(f2.read())
        hash2 = the_md5.hexdigest()
        f1.close()
        f2.close()

        if hash1 == hash2:
            with open(log,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['delete',file1,os.path.join(frfolder,file1),os.path.join(dest,file1),os.path.getsize(os.path.join(frfolder,file1)),hash1])
                f.close()
            os.remove(os.path.join(frfolder,file1))
            print("remove,"+ os.path.join(frfolder,file1) )
        else:
            serialnumber = 1
            while os.path.exists(os.path.join(dest,os.path.splitext(file1)[0] + '-' + str(serialnumber) + os.path.splitext(file1)[1])):
                serialnumber = serialnumber + 1
            newfile = os.path.splitext(file1)[0] + '-'+ str(serialnumber) + os.path.splitext(file1)[1] 
            print("new file name:"+ newfile)

            with open(log,'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['rename',file1,os.path.join(frfolder,file1),os.path.join(dest,newfile),os.path.getsize(os.path.join(frfolder,file1)),hash1])
                f.close()
            shutil.move(os.path.join(frfolder,file1),os.path.join(dest,newfile))
            print("shutil move,"+ "from,"+ os.path.join(frfolder,file1)+ ",to,"+ os.path.join(dest,newfile) )


    else:
        the_md5=hashlib.md5()
        f1 = open(os.path.join(frfolder,file1), 'rb')
        the_md5.update(f1.read())
        hash1 = the_md5.hexdigest()
        f1.close()
        
        with open(log,'a',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['move',file1,os.path.join(frfolder,file1),os.path.join(dest,file1),os.path.getsize(os.path.join(frfolder,file1)),hash1])
            f.close()
        shutil.move(os.path.join(frfolder,file1),dest)
        print("shutil move,"+ "from,"+ os.path.join(frfolder,file1)+ ",to,"+ dest)


def gettime(file):
    """Get embedded EXIF data from image file."""
    ret = {}
    if filetype.guess(file) is not None:
        if filetype.guess(file).extension in ('jpg','jpeg','gif','png','bmp'):    
            try:
                img = Image.open(file)
                if hasattr( img, '_getexif' ):
                    try:
                        exifinfo = img._getexif()
                    except:
                        exifinfo = None
                    if exifinfo != None:
                        for tag, value in exifinfo.items():
                            decoded = TAGS.get(tag, tag)
                            ret[decoded] = value
                    else:
                        timeArray = time.localtime(os.path.getctime(file))
                        otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
                        return str(otherStyleTime).replace(':','-').replace(' ','_')
            except IOError:
                print('IOERROR/ValueError ' + file)


            
    if ret.get('DateTimeOriginal') != None:
        cd = ret.get('DateTimeOriginal')[0:7].replace(':','-').replace(' ','')
        return cd
    else:
        timeArray = time.localtime(os.path.getctime(file))
        otherStyleTime = time.strftime("%Y-%m-%d-%H%M%S", timeArray)
        return str(otherStyleTime).replace(':','-').replace(' ','_')
#        print('creation date: '+os.path.getctime(fname).replace(':','-').replace(' ','_') ) 
#        return os.path.getctime(fname).replace(':','-').replace(' ','_')   


def getmaker(file):
    """Get embedded EXIF data from image file."""
    ret = {}
    if filetype.guess(file) is not None:
        if filetype.guess(file).extension in ('jpg','jpeg','gif','png','bmp'):    
            try:
                img = Image.open(file)
                if hasattr( img, '_getexif' ):
                    try:
                        exifinfo = img._getexif()
                    except:
                        exifinfo = None
                    if exifinfo != None:
                        for tag, value in exifinfo.items():
                            decoded = TAGS.get(tag, tag)
                            ret[decoded] = value
                    else:
                        return "default"
            except IOError:
                print('IOERROR/ValueError ' + file)            
    if ret.get('Make') != None and ret.get('Model') != None:
        return str(ret.get('Make')).replace(' ','').replace(chr(0),'') + "-" + str(ret.get('Model')).replace(' ','').replace(chr(0),'')
    elif ret.get('Make') != None:        
        return str(ret.get('Make')).replace(' ','').replace(chr(0),'')
    elif ret.get('Model') != None:
        return str(ret.get('Model')).replace(' ','').replace(chr(0),'')
    else:
        return "default"



def get_size(file):
    return os.path.getsize(file)


def main():
    pass
if __name__ == '__main__':
    main()
