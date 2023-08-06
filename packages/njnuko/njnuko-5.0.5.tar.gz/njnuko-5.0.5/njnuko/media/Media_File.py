import json
import requests
import hashlib
import os
import exiftool
import datetime
import time


class Media_File:


    def __init__(self,file_loc):
        self.file_loc = file_loc
        self.log =os.path.join("~","_" + self.file_loc+".log")

    
    def get_md5(self):
        the_md5=hashlib.md5()
        hash = ''
        with open(self.file_loc,'rb') as f:
            the_md5.update(f.read())
            hash = the_md5.hexdigest()
        return hash

    def get_metadata(self):
        """
        EXIF:Model
        File:MIMEType
        EXIF:Make
        """
        metadata = ""
        with exiftool.ExifTool() as et:
            metadata = et.get_metadata(self.file_loc)
        return metadata

    def get_type(self):
        exif = self.get_metadata()
        if exif.get("File:FileType") is None:
            if os.path.splitext(self.file_loc)[1][1:].upper() != "":
                return os.path.splitext(self.file_loc)[1][1:].upper()
            else:
                return "NON"
        else:
            return exif.get("File:FileType")
        return "NON"

    def get_create_date(self):
        exif = self.get_metadata()
        if exif.get("EXIF:CreateDate"):
            a = exif.get("EXIF:CreateDate")[0:10]
            b = a.replace(":","-")
            return b
        elif exif.get("QuickTime:CreateDate"):
            a = exif.get("QuickTime:CreateDate")[0:10]
            b = a.replace(":","-")
            return b
        else:
            pass
        create_time =datetime.datetime.strptime(time.ctime(os.path.getctime(self.file_loc)), "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%d")
        return create_time

    def get_geo_address(self):
        dict={}
        exif = self.get_metadata()
        if exif.get("Composite:GPSLatitude") is not None:
            geo='{:.4f}'.format(exif.get("Composite:GPSLongitude"))+","+'{:.4f}'.format(exif.get("Composite:GPSLatitude"))
            gaode=json.load(open(os.path.join(os.path.dirname(os.getcwd()),"config","gaode.json")))
            base=gaode.get("base")
            key = gaode.get("key")
            parameters={"location":geo,"key":key}
            try:
                response = requests.get(base, parameters)
                if response.status_code == 200:
                    address = response.json()
                    dict["city"]=address.get("regeocode").get("addressComponent").get("city")
                    dict["province"]=address.get("regeocode").get("addressComponent").get("province")
                    dict["district"]=address.get("regeocode").get("addressComponent").get("district")
                    dict["country"]=address.get("regeocode").get("addressComponent").get("country")
                    dict["address"]=address.get("regeocode").get("formatted_address")
                else:
                    pass
            except:
                pass
            return dict

