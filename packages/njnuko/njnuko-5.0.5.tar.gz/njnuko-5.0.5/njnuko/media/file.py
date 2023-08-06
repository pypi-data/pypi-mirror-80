from Media_File import Media_File
from PIL import Image
import imagehash
def is_similar(src_file,cmp_file):
    """
    返回same如果相同
    返回similar如果相似
    返回空如果不同
    """
    media1 = Media_File(src_file)
    hash1= media1.get_md5()
    media2= Media_File(cmp_file)
    hash2=media2.get_md5()
    status = ""
    if hash1==hash2:
        status = "same"
    else:
        hash11 =  imagehash.average_hash(Image.open(src_file))
        hash12 =  imagehash.average_hash(Image.open(cmp_file))
        if (hash11 == hash12):
            status = "similar"
    return status

def file_move(file1,dest):
        media1 = Media_File(file1)
        hash1=media1.get_md5()
        log=""
        if os.path.exists(os.path.join(dest,os.path.basename(file1))):
            media2 = Media_File(os.path.join(dest,os.path.basename(file1)))
            hash2=media2.get_md5()
            if hash1 == hash2:
                log=['delete',file1,os.path.join(frfolder,file1),os.path.join(dest,file1),os.path.getsize(os.path.join(frfolder,file1)),hash1]
                os.remove(os.path.join(frfolder,file1))
            else:
                new_file_name  = os.path.join(dest,os.path.splitext(os.path.basename(file1))[0] + "_1" + os.path.splitext(file1)[1])
                while os.path.exists(new_file_name):
                    new_file_name  = os.path.join(dest,os.path.splitext(os.path.basename(new_file_name))[0] + "_1" + os.path.splitext(new_file_name)[1])
                shutil.move(file1,os.path.join(new_file_name))
                print("shutil move,"+ "from,"+ file1+ ",to,"+ new_file_name )
                log=['rename',os.path.basename(file1),file1,new_file_name,os.path.getsize(new_file_name),hash1]
        else:
            shutil.move(file1,os.path.join(dest,os.path.basename(file1)))
            print("shutil move,"+ "from,"+ file1+ ",to,"+ os.path.join(dest,os.path.basename(file1)))
            log=['rename',os.path.basename(file1),file1,new_file_name,os.path.getsize(file1),hash1]
        return log
