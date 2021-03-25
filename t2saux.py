import os
import sys
#import shutil
import time


#Variables
log_path="/home/pi/logs/"      # path to save historical data  --- > RPi
last_hour = -1
msg_complete = True
separator = ' -- '


def getdate():
    year = '%04d' %(time.localtime().tm_year)
    month = '%02d' %(time.localtime().tm_mon)
    day = '%02d' %(time.localtime().tm_mday)
    hour = '%02d' %(time.localtime().tm_hour)
    minute = '%02d' %(time.localtime().tm_min)
    second = '%02d' %(time.localtime().tm_sec)

    return year, month, day, hour, minute, second

def prefix():
    year, month, day, hour, minute, second = getdate()
    timestamp = '%s/%s/%s %s:%s:%s%s'  %(year, month, day, hour, minute, second, separator)
    return timestamp


def checkpath(year, month, base_path = log_path):
    # Define path and files names based on current date
    year_path = '%s%s/' %(base_path, year)
    month_path = '%s%s/%s/' %(base_path, year, month)

    #uid, gid = userugid()

    "check if current Year folder is created"
    try:
        os.listdir(year_path)
    except OSError:
        os.mkdir(year_path)
        #os.chown(year_path, 1000, 1000)  # it should be os.chown(year_path,uid, gid)

    "check if current Month folder is created"
    try:
        os.listdir(month_path)
    except OSError:
        os.mkdir(month_path)
        #os.chown(month_path, 1000, 1000) # it should be os.chown(month_path, uid, gid)

    return month_path


def file_open(suffixname = 'serial', base_path = log_path):


    year, month, day, hour, minute, second = getdate()
    path = checkpath(year, month, base_path)
    file_name = '%s-%s-%s_%sH_%s.log' %(year, month, day, hour, suffixname)
    path_file = '%s%s' %(path, file_name)

    "check if file already exists..."
    try:
        dirlist = os.listdir(path)
    except OSError:
        print('path error')
        return 'path error'

    file_is_new = True
    for i in dirlist:
        if i == file_name :
            file_is_new = False
            break
            
    global fout
    fout = open(path_file, 'at')
    

if (last_hour == -1):
    file_open()


def file_close():

    fout.close()


def write(data, msg_complete):
    year, month, day, hour, minute, second = getdate()
    
    if (last_hour != hour):
        file_close()
        file_open()

    if type(data) != str :
        line = ''
        if msg_complete : 
            line = line + prefix()
        for i in range(len(data)) :
            line = line + chr(data[i])
            if data[i] == 10 and i < len(data)-1: 
                #print('new line')
                line = line + prefix()
        #print(line)
        #print('LAST_CHAR', str(n), '|')
        fout.write(line)
        if data[i] ==10 :
            msg_complete = True
        else:
            msg_complete = False
        return msg_complete
    else:
        line = data
    
        if line[:-1] !='\n': 
            line = line + '\n'

        sentence = '%s%s' %(prefix(), line)

        fout.write(sentence)

        return True



def main():
    print (""" this package should be import into your python main.py file and invoque the functions define here
    """)
if __name__ == '__main__':
    main()


