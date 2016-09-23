#coding:utf-8
import time,os,sys
from django.conf import settings
'''文件上传'''
def handle_uploaded_file(f,username):
    file_name = ""

    try:
        path =str(settings.MEDIA_ROOT)
        
        if not os.path.exists(path):
            os.makedirs(path)
        new_name=username+'.jpg'
        file_name = path + '/'+ new_name
        
        print file_name
        destination = open(file_name, 'wb+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
                
    except Exception, e:
        return 'False',e

    return new_name